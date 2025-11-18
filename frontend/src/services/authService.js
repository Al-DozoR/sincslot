import api from "../api/axios";

export const authService = {
  register: async (data) => {
    const response = await api.post("/register", data);
    return response.data;
  },

  refreshToken: async () => {
    const response = await api.post("/refresh-token", {}, { withCredentials: true });
    return response.data;
  },

  forgotPassword: async (email) => {
    const response = await api.post("/forgot-password", { email });
    return response.data;
  },
};