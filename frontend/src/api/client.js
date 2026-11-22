const BASE_URL = '/api';

export async function analyzeText(text, language = 'auto', saveHistory = true) {
  const res = await fetch(`${BASE_URL}/analyze/text`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, language, save_history: saveHistory })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Text analysis failed');
  }
  return res.json();
}

export async function analyzeUrl(url, saveHistory = true) {
  const res = await fetch(`${BASE_URL}/analyze/url`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, save_history: saveHistory })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'URL analysis failed');
  }
  return res.json();
}

export async function analyzeImage(formData) {
  const res = await fetch(`${BASE_URL}/analyze/image`, {
    method: 'POST',
    body: formData
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Image analysis failed');
  }
  return res.json();
}

export async function chatAssistant(message, language = 'en', history = []) {
  const res = await fetch(`${BASE_URL}/assistant/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, language, history })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Assistant request failed');
  }
  return res.json();
}

export async function submitThreatReport(reportData) {
  const res = await fetch(`${BASE_URL}/report`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(reportData)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to submit report');
  }
  const data = await res.json();
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new CustomEvent('upi-admin-alert-trigger', {
      detail: {
        type: 'case_filed',
        category: reportData.scam_category || 'general_fraud',
        title: `🚨 New Case Filed: ${(reportData.scam_category || 'general_fraud').replace(/_/g, ' ').toUpperCase()}`,
        content: reportData.suspicious_content || '',
        comments: reportData.comments || '',
        timestamp: new Date().toISOString()
      }
    }));
  }
  return data;
}

export async function getAdminAlerts(limit = 30) {
  const res = await fetch(`${BASE_URL}/dashboard/alerts?limit=${limit}`);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to fetch admin alerts');
  }
  return res.json();
}

export async function markAdminAlertsRead() {
  const res = await fetch(`${BASE_URL}/dashboard/alerts/mark-read`, {
    method: 'POST'
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to mark alerts as read');
  }
  return res.json();
}

export async function getDashboardStats(scope = 'all') {
  const res = await fetch(`${BASE_URL}/dashboard/stats?scope=${scope}`);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to load dashboard statistics');
  }
  return res.json();
}

export async function getHistory(filterType = 'all', limit = 25, offset = 0) {
  const res = await fetch(`${BASE_URL}/history?filter_type=${filterType}&limit=${limit}&offset=${offset}`);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to load history');
  }
  return res.json();
}

export async function loginAdmin(email, password) {
  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Invalid email or password');
  }
  return res.json();
}

export async function getAdminMe(token) {
  const res = await fetch(`${BASE_URL}/auth/me`, {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  if (!res.ok) {
    throw new Error('Unauthorized');
  }
  return res.json();
}

export async function analyzeVpa(vpa, payeeName = '', amount = null, isCollect = false) {
  const res = await fetch(`${BASE_URL}/analyze/vpa`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      vpa,
      payee_name: payeeName,
      amount: amount ? parseFloat(amount) : null,
      is_collect: isCollect
    })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'VPA analysis failed');
  }
  return res.json();
}

export async function analyzeBatch(items) {
  const res = await fetch(`${BASE_URL}/analyze/batch`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ items })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Batch analysis failed');
  }
  return res.json();
}

export async function submitFeedback(feedbackData) {
  const res = await fetch(`${BASE_URL}/feedback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(feedbackData)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to submit feedback');
  }
  const data = await res.json();
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new CustomEvent('upi-admin-alert-trigger', {
      detail: {
        type: 'user_feedback',
        title: `💬 User Feedback: ${feedbackData.is_correct ? 'Confirmed Correct' : 'Reported Correction'}`,
        content: feedbackData.input_text || '',
        comments: feedbackData.feedback_notes || '',
        is_correct: feedbackData.is_correct,
        timestamp: new Date().toISOString()
      }
    }));
  }
  return data;
}

export async function getHealth() {
  const res = await fetch(`${BASE_URL}/health`);
  if (!res.ok) {
    throw new Error('Health check failed');
  }
  return res.json();
}

export async function lookupReputation(entityType, entityValue) {
  const params = new URLSearchParams({ entity_type: entityType, entity_value: entityValue });
  const res = await fetch(`${BASE_URL}/reputation/lookup?${params.toString()}`);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Reputation lookup failed');
  }
  return res.json();
}

export async function submitCommunityReport(reportData) {
  const res = await fetch(`${BASE_URL}/reputation/report`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(reportData)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to submit community report');
  }
  const data = await res.json();
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new CustomEvent('upi-admin-alert-trigger', {
      detail: {
        type: 'community_flag',
        title: `⚠️ Flagged Entity: ${reportData.entity_value} (${reportData.entity_type})`,
        content: reportData.evidence_text || '',
        category: reportData.scam_category,
        timestamp: new Date().toISOString()
      }
    }));
  }
  return data;
}

export async function submitReputationDispute(disputeData) {
  const res = await fetch(`${BASE_URL}/reputation/dispute`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(disputeData)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to submit dispute');
  }
  return res.json();
}

export async function getPendingModeration(token) {
  const res = await fetch(`${BASE_URL}/reputation/admin/pending`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to fetch moderation queue');
  }
  return res.json();
}

export async function resolveModerationReport(reportId, action, token) {
  const res = await fetch(`${BASE_URL}/reputation/admin/resolve`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ report_id: reportId, action })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to resolve report');
  }
  return res.json();
}

export async function resolveModerationDispute(disputeId, action, token) {
  const res = await fetch(`${BASE_URL}/reputation/admin/resolve-dispute`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    },
    body: JSON.stringify({ dispute_id: disputeId, action })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to resolve dispute');
  }
  return res.json();
}

export async function seedDemoModeration(token) {
  const res = await fetch(`${BASE_URL}/reputation/admin/seed-demo`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to seed demo moderation items');
  }
  return res.json();
}

export async function exportStudyCsv(token) {
  const res = await fetch(`${BASE_URL}/study/export`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to export study CSV');
  }
  return res.blob();
}


