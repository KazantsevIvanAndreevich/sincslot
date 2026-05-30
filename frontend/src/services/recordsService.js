import api from "../api/axios";

export const recordsService = {
  getRecords: async () => {
    const response = await api.get("/records");
    return response.data;
  },
};
