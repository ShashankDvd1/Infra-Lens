/**
 * API Client for interacting with the FastAPI backend.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const API_PREFIX = '/api/v1';

/**
 * Generic fetch wrapper.
 */
export async function fetchAPI(endpoint: string, options: RequestInit = {}) {
  const url = `${API_URL}${API_PREFIX}${endpoint}`;
  const response = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`API Error: ${response.status} ${response.statusText} - ${errorBody}`);
  }

  return response.json();
}

/**
 * Project Endpoints
 */
export const getProjects = (params?: {
  city?: string;
  project_type?: string;
  status?: string;
  page?: number;
}) => {
  const queryParams = new URLSearchParams();
  if (params?.city) queryParams.append('city', params.city);
  if (params?.project_type) queryParams.append('project_type', params.project_type);
  if (params?.status) queryParams.append('status', params.status);
  if (params?.page) queryParams.append('page', params.page.toString());

  const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
  return fetchAPI(`/projects${queryString}`);
};

export const getProjectDetail = (id: string) => {
  return fetchAPI(`/projects/${id}`);
};

/**
 * Map Endpoints
 */
export const getMapMarkers = (params?: { city?: string; project_type?: string; status?: string }) => {
  const queryParams = new URLSearchParams();
  if (params?.city) queryParams.append('city', params.city);
  if (params?.project_type) queryParams.append('project_type', params.project_type);
  if (params?.status) queryParams.append('status', params.status);

  const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
  return fetchAPI(`/map/markers${queryString}`);
};

/**
 * Search Endpoints
 */
export const searchAll = (q: string) => {
  const queryParams = new URLSearchParams({ q });
  return fetchAPI(`/search?${queryParams.toString()}`);
};

/**
 * AI Endpoints
 */
export const askAI = (query: string) => {
  return fetchAPI(`/ai/ask`, {
    method: 'POST',
    body: JSON.stringify({ query }),
  });
};
