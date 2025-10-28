import React, { useState } from 'react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

function AuthPage({ onLogin }) {
<<<<<<< HEAD
  const [activeTab, setActiveTab] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
=======
  const [step, setStep] = useState('phone'); // 'phone' or 'otp'
  const [phoneNumber, setPhoneNumber] = useState('');
  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [otpSent, setOtpSent] = useState(false);

  const handleSendOTP = async (e) => {
>>>>>>> c7ba531 (Initial push: migrate local codebase to KisanMitr)
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
<<<<<<< HEAD
      const endpoint = activeTab === 'login' ? '/auth/login' : '/auth/register';
      const response = await axios.post(`${API}${endpoint}`, {
        email,
        password,
      });

      const { access_token, user_id, email: userEmail } = response.data;
      onLogin(access_token, { user_id, email: userEmail });
    } catch (err) {
      setError(
        err.response?.data?.detail || 
        `Failed to ${activeTab}. Please try again.`
=======
      console.log('Sending OTP to:', phoneNumber);
      const response = await axios.post(`${API}/auth/send-otp`, {
        phone_number: phoneNumber,
      });

      if (response.data.success) {
        setOtpSent(true);
        setStep('otp');
        setError('');
      }
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Failed to send OTP. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOTP = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      console.log('Verifying OTP:', otp, 'for phone:', phoneNumber);
      const response = await axios.post(`${API}/auth/verify-otp`, {
        phone_number: phoneNumber,
        otp: otp,
      });

      const { access_token, user_id, phone_number: userPhone, is_new_user } = response.data;
      onLogin(access_token, { user_id, phone_number: userPhone, is_new_user });
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Invalid OTP. Please try again.'
>>>>>>> c7ba531 (Initial push: migrate local codebase to KisanMitr)
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
<<<<<<< HEAD
=======
      <style jsx>{`
        .auth-button-secondary {
          background: transparent;
          color: #666;
          border: 1px solid #ddd;
          margin-top: 10px;
        }
        .auth-button-secondary:hover {
          background: #f5f5f5;
        }
        .auth-header h2 {
          margin-bottom: 8px;
          color: #2d5016;
        }
        .auth-header p {
          color: #666;
          margin-bottom: 20px;
        }
        .form-group small {
          color: #666;
          font-size: 12px;
          margin-top: 4px;
          display: block;
        }
      `}</style>
>>>>>>> c7ba531 (Initial push: migrate local codebase to KisanMitr)
      <div className="auth-layout">
        {/* Left Column - Metrics */}
        <div className="auth-metrics-column">
          <div className="metrics-container">
            <div className="metric-box">
              <div className="metric-icon">♻️</div>
              <div className="metric-value">20 Tonnes</div>
              <div className="metric-label">Waste Prevented</div>
            </div>
            <div className="metric-box">
              <div className="metric-icon">👨‍🌾</div>
              <div className="metric-value">1,00,000+</div>
              <div className="metric-label">Farmers Helped</div>
            </div>
            <div className="metric-box">
              <div className="metric-icon">💰</div>
              <div className="metric-value">₹185 Crores</div>
              <div className="metric-label">Subsidy Allotment</div>
            </div>
          </div>
        </div>

        {/* Right Column - Auth Form */}
        <div className="auth-form-column">
          <div className="auth-container">
            <div className="auth-logo">
              <h1>🌾 Farmer Chatbot</h1>
              <p>Your AI-powered agricultural assistant</p>
            </div>

<<<<<<< HEAD
            <div className="auth-tabs">
              <button
                className={`auth-tab ${activeTab === 'login' ? 'active' : ''}`}
                onClick={() => {
                  setActiveTab('login');
                  setError('');
                }}
                data-testid="login-tab"
              >
                Login
              </button>
              <button
                className={`auth-tab ${activeTab === 'register' ? 'active' : ''}`}
                onClick={() => {
                  setActiveTab('register');
                  setError('');
                }}
                data-testid="register-tab"
              >
                Sign Up
              </button>
            </div>

            <form className="auth-form" onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                  id="email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="your@email.com"
                  required
                  data-testid="email-input"
                />
              </div>

              <div className="form-group">
                <label htmlFor="password">Password</label>
                <input
                  id="password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                  minLength={6}
                  data-testid="password-input"
                />
              </div>

              {error && (
                <div className="error-message" data-testid="error-message">
                  {error}
                </div>
              )}

              <button
                type="submit"
                className="auth-button"
                disabled={loading}
                data-testid="auth-submit-button"
              >
                {loading
                  ? 'Please wait...'
                  : activeTab === 'login'
                  ? 'Login'
                  : 'Create Account'}
              </button>
            </form>
=======
            <div className="auth-header">
              <h2>
                {step === 'phone' ? 'Enter Phone Number' : 'Verify OTP'}
              </h2>
              <p>
                {step === 'phone'
                  ? 'We\'ll send you a verification code'
                  : `Code sent to ${phoneNumber}`}
              </p>
            </div>

            {step === 'phone' ? (
              <form className="auth-form" onSubmit={handleSendOTP}>
                <div className="form-group">
                  <label htmlFor="phone">Phone Number</label>
                  <input
                    id="phone"
                    type="tel"
                    value={phoneNumber}
                    onChange={(e) => setPhoneNumber(e.target.value)}
                    placeholder="+91 98765 43210"
                    required
                    data-testid="phone-input"
                  />
                  <small>Enter your 10-digit mobile number</small>
                </div>

                {error && (
                  <div className="error-message" data-testid="error-message">
                    {error}
                  </div>
                )}

                <button
                  type="submit"
                  className="auth-button"
                  disabled={loading}
                  data-testid="send-otp-button"
                >
                  {loading ? 'Sending OTP...' : 'Send OTP'}
                </button>
              </form>
            ) : (
              <form className="auth-form" onSubmit={handleVerifyOTP}>
                <div className="form-group">
                  <label htmlFor="otp">Enter OTP</label>
                  <input
                    id="otp"
                    type="text"
                    value={otp}
                    onChange={(e) => setOtp(e.target.value)}
                    placeholder="OTP"
                    required
                    maxLength={4}
                    data-testid="otp-input"
                    style={{ textAlign: 'center', fontSize: '24px', letterSpacing: '8px' }}
                  />
                  <small>Enter the 4-digit code (Use: 7421)</small>
                </div>

                {error && (
                  <div className="error-message" data-testid="error-message">
                    {error}
                  </div>
                )}

                <button
                  type="submit"
                  className="auth-button"
                  disabled={loading}
                  data-testid="verify-otp-button"
                >
                  {loading ? 'Verifying...' : 'Verify & Login'}
                </button>

                <button
                  type="button"
                  className="auth-button-secondary"
                  onClick={() => {
                    setStep('phone');
                    setOtp('');
                    setError('');
                  }}
                  data-testid="back-button"
                >
                  Change Phone Number
                </button>
              </form>
            )}
>>>>>>> c7ba531 (Initial push: migrate local codebase to KisanMitr)
          </div>
        </div>
      </div>
    </div>
  );
}

export default AuthPage;
