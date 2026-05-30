import api from "../api/axios.js";

const BASE_URL = "/api/v1/company";

export const servicesService = {
  //Создать услугу
  create: async (data) => {
    const response = await api.post(`${BASE_URL}/service/`, data);
    return response.data;
  },

  //Получить услугу по id
  get: async (id) => {
    const response = await api.get(`${BASE_URL}/service/${id}`);
    return response.data;
  },

  //Обновить услугу
  update: async (id, data) => {
    const response = await api.patch(`${BASE_URL}/service/${id}`, data);
    return response.data;
  },

  //Удалить услугу
  delete: async (id) => {
    const response = await api.delete(`${BASE_URL}/service/${id}`);
    return response.data;
  }
};
