import api from "../api/axios.js";

const BASE_URL = '/api/v1/company';

export const companyService = {

  async getCompanySettings() {
    const response = await api.get(`${BASE_URL}/settings/`);
    return response.data;
  },

  async updateCompanySettings(companyData) {
    const response = await api.patch(`${BASE_URL}/settings/`, companyData);
    return response.data;
  },

  async getCompanySchedule() {
    const response = await api.get(`${BASE_URL}/work-schedule/`);
    return response.data;
  },

  async updateCompanySchedule(schedulePayload) {
    const response = await api.post(`${BASE_URL}/work-schedule/`, schedulePayload);
    return response.data;
  },

  async uploadCompanyLogo(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await api.put(`${BASE_URL}/logo-image/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    return response.data;
  },

  async getCompanyLogo() {
    const response = await api.get(`${BASE_URL}/logo-image/`, {
      responseType: "blob",
    });

    const contentType = response.headers["content-type"];

    if (contentType?.includes("application/json")) {
      const text = await response.data.text();
      const json = JSON.parse(text);

      return { error: json.error || "Logo not found" };
    }

    if (contentType?.includes("image")) {
      return URL.createObjectURL(response.data);
    }

    return { error: "Unknown response type" };
  },

  async deactivateCompany() {
    const response = await api.post(
      `${BASE_URL}/settings/deactivate`,
      {}
    );
    return response.data;
  }
};
