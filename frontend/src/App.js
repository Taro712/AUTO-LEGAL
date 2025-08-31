import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, MessageSquare, Trash2, CheckCircle, AlertCircle } from 'lucide-react';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [status, setStatus] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [isQuerying, setIsQuerying] = useState(false);
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [error, setError] = useState('');
  const [vectorStoreExists, setVectorStoreExists] = useState(false);

  useEffect(() => {
    checkStatus();
  }, []);

  const checkStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/status`);
      setVectorStoreExists(response.data.vector_store_exists);
      setStatus(response.data.message);
    } catch (err) {
      console.error('Error checking status:', err);
      setError('Failed to check status');
    }
  };

  const onDrop = async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    const file = acceptedFiles[0];
    setIsUploading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setStatus(response.data.message);
      setVectorStoreExists(true);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed');
    } finally {
      setIsUploading(false);
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc'],
      'image/*': ['.png', '.jpg', '.jpeg'],
      'text/plain': ['.txt'],
    },
    multiple: false,
  });

  const handleQuery = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setIsQuerying(true);
    setError('');
    setResponse('');

    const formData = new FormData();
    formData.append('query', query);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/query`, formData);
      setResponse(response.data.result);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Query failed');
    } finally {
      setIsQuerying(false);
    }
  };

  const handleReset = async () => {
    try {
      await axios.delete(`${API_BASE_URL}/api/reset`);
      setVectorStoreExists(false);
      setStatus('Vector store reset successfully');
      setResponse('');
      setError('');
    } catch (err) {
      setError('Failed to reset vector store');
    }
  };

  return (
    <div className="container">
      <header className="card">
        <h1 style={{ textAlign: 'center', marginBottom: '16px', color: '#1f2937' }}>
          <FileText size={32} style={{ marginRight: '12px', verticalAlign: 'middle' }} />
          AUTOLEGAL
        </h1>
        <p style={{ textAlign: 'center', color: '#6b7280', fontSize: '18px' }}>
          AI-powered legal document analysis and Q&A
        </p>
      </header>

      {/* Status Card */}
      <div className="card">
        <h2 style={{ marginBottom: '16px', color: '#1f2937' }}>
          <CheckCircle size={24} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
          System Status
        </h2>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', flexWrap: 'wrap' }}>
          <span className={`status ${vectorStoreExists ? 'success' : 'info'}`}>
            {vectorStoreExists ? 'Document Ready' : 'No Document Loaded'}
          </span>
          {status && (
            <span className="status info">
              {status}
            </span>
          )}
          {vectorStoreExists && (
            <button onClick={handleReset} className="btn" style={{ background: '#dc2626' }}>
              <Trash2 size={16} style={{ marginRight: '8px' }} />
              Reset
            </button>
          )}
        </div>
      </div>

      {/* File Upload Card */}
      <div className="card">
        <h2 style={{ marginBottom: '16px', color: '#1f2937' }}>
          <Upload size={24} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
          Upload Document
        </h2>
        <div
          {...getRootProps()}
          className={`dropzone ${isDragActive ? 'active' : ''}`}
        >
          <input {...getInputProps()} />
          {isUploading ? (
            <div>
              <div className="loading" style={{ margin: '0 auto 16px' }}></div>
              <p>Processing document...</p>
            </div>
          ) : (
            <div>
              <Upload size={48} style={{ marginBottom: '16px', color: '#667eea' }} />
              <p style={{ fontSize: '18px', marginBottom: '8px', color: '#374151' }}>
                {isDragActive ? 'Drop the file here' : 'Drag & drop a file here, or click to select'}
              </p>
              <p style={{ color: '#6b7280' }}>
                Supports: PDF, DOCX, DOC, PNG, JPG, JPEG, TXT
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Query Card */}
      {vectorStoreExists && (
        <div className="card">
          <h2 style={{ marginBottom: '16px', color: '#1f2937' }}>
            <MessageSquare size={24} style={{ marginRight: '8px', verticalAlign: 'middle' }} />
            Ask Questions
          </h2>
          <form onSubmit={handleQuery} style={{ marginBottom: '16px' }}>
            <div style={{ display: 'flex', gap: '12px' }}>
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask a question about your document..."
                className="input"
                style={{ flex: 1 }}
              />
              <button
                type="submit"
                className="btn"
                disabled={isQuerying || !query.trim()}
              >
                {isQuerying ? (
                  <div className="loading" style={{ width: '16px', height: '16px' }}></div>
                ) : (
                  'Ask'
                )}
              </button>
            </div>
          </form>

          {response && (
            <div style={{ 
              background: '#f8fafc', 
              padding: '16px', 
              borderRadius: '8px', 
              border: '1px solid #e2e8f0' 
            }}>
              <h3 style={{ marginBottom: '12px', color: '#1f2937' }}>Answer:</h3>
              <p style={{ lineHeight: '1.6', color: '#374151' }}>{response}</p>
            </div>
          )}
        </div>
      )}

      {/* Error Display */}
      {error && (
        <div className="card" style={{ border: '2px solid #fecaca' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <AlertCircle size={20} color="#dc2626" />
            <span style={{ color: '#dc2626', fontWeight: '600' }}>Error:</span>
            <span style={{ color: '#374151' }}>{error}</span>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
