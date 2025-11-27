import api from "../api/axios";

export const authService = {
  register: async (data) => {
    const response = await api.post("/api/v1/company/register", data);
    return response.data;
  },

  refreshToken: async () => {
    const response = await api.post("/api/v1/company/refresh-token", {}, { withCredentials: true });
    return response.data;
  },

  forgotPassword: async (email) => {
    const response = await api.post("/api/v1/company/recover", { email });
    return response.data;
  },

  checkToken: async (token) => {
    const response = await api.get("/health-auth");
    return response.data;
  },

  login: async (data) => {
    const response = await api.post("/api/v1/company/login", data);
    return response.data;
  }
};