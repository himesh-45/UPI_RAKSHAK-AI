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

export async function chatAssistant(message, language = 'en') {
  const res = await fetch(`${BASE_URL}/assistant/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, language })
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
  return res.json();
}

export async function getHealth() {
  const res = await fetch(`${BASE_URL}/health`);
  if (!res.ok) {
    throw new Error('Health check failed');
  }
  return res.json();
}

