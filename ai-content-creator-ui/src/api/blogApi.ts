import axios from "axios";

const BASE_URL = "http://localhost:8000"; // replace with your deployed URL if needed

export const generateBlog = async (data: {
  topic: string;
  tone: string;
  audience: string;
  outline?: string;
}) => {
  const response = await axios.post(`${BASE_URL}/generate`, data);
  return response.data;
};

export const checkTopic = async (slug: string, topic: string) => {
  const response = await axios.get(`${BASE_URL}/check-topic`, {
    params: { slug, topic },
  });
  return response.data;
};

export const suggestTopics = async (category: string) => {
  const response = await axios.get(`${BASE_URL}/suggest-topics`, {
    params: { category },
  });
  return response.data;
};

export const saveBlog = async (data: {
  topic: string;
  blog: string;
  captions: string;
  citations: string;
}) => {
  const response = await axios.post(`${BASE_URL}/save`, data);
  return response.data;
};

export const getCalendarData = async () => {
  const response = await axios.get(`${BASE_URL}/calendar`);
  return response.data;
};

export const getAnalyticsData = async () => {
  const response = await fetch("http://localhost:8000/analytics"); // Change base URL if needed
  if (!response.ok) {
    throw new Error("Failed to fetch analytics data");
  }
  return response.json();
};
