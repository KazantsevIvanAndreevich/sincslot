import api from "../api/axios";

export const authService = {
  register: async (data) => {
    const response = await api.post("/api/v1/company/auth/register", data);
    return response.data;
  },

  refreshToken: async () => {
    const response = await api.post("/api/v1/company/auth/refresh-token", {}, { withCredentials: true });
    return response.data;
  },

  forgotPassword: async (email) => {
    const response = await api.post("/api/v1/company/auth/recover", { email });
    return response.data;
  },

  checkToken: async (token) => {
    const response = await api.get("/health-auth");
    return response.data;
  },

  login: async (data) => {
    const response = await api.post("/api/v1/company/auth/login", data);
    return response.data;
  },

  logout: () => {
    return axios.delete(
      "/api/v1/company/auth/logout",
      { withCredentials: true }
    );
  }
};
