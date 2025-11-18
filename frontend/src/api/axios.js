import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:4000",
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });

  failedQueue = [];
};

api.interceptors.response.use(
  response => response,
  async (error) => {
    const originalRequest = error.config;

    // если запрос на refresh-token, просто отклоняем
    if (originalRequest.url.includes("/refresh-token")) {
      return Promise.reject(error);
    }

    if (error.response?.status === 401) {
      if (!isRefreshing) {
        isRefreshing = true;
        try {
          const { data } = await axios.post("http://localhost:4000/refresh-token", {}, { withCredentials: true });
          localStorage.setItem("token", data.accessToken);
          isRefreshing = false;
          processQueue(null, data.accessToken);
        } catch (err) {
          isRefreshing = false;
          processQueue(err, null);
          return Promise.reject(err);
        }
      }

      return new Promise((resolve, reject) => {
        failedQueue.push({
          resolve: (token) => {
            originalRequest.headers["Authorization"] = "Bearer " + token;
            resolve(api(originalRequest));
          },
          reject: (err) => reject(err)
        });
      });
    }

    return Promise.reject(error);
  }
);

export default api;