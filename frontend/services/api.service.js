import axios from 'axios'
import Cookies from 'js-cookie'
import {baseURL} from '~/global';

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

class ApiService {
  constructor() {
    this.instance = axios.create({
      baseURL,
      withCredentials: true,
      withXSRFToken: true,
    })
  }

  request(method, url, data = {}, config = {}) {
    return this.instance({
      method,
      url,
      data,
      ...config
    })
  }

  get(url, config = {}) {
    return this.request('GET', url, {}, {...config, headers: {'X-CSRFToken': Cookies.get('csrftoken'), ...(config.headers ?? {})}})
  }

  post(url, data, config = {}) {
    return this.request('POST', url, data, {...config, headers: {'X-CSRFToken': Cookies.get('csrftoken'), ...(config.headers ?? {})}})
  }

  put(url, data, config = {}) {
    return this.request('PUT', url, data, {...config, headers: {'X-CSRFToken': Cookies.get('csrftoken'), ...(config.headers ?? {})}})
  }

  patch(url, data, config = {}) {
    return this.request('PATCH', url, data, {...config, headers: {'X-CSRFToken': Cookies.get('csrftoken'), ...(config.headers ?? {})}})
  }

  delete(url, data = {}, config = {}) {
    return this.request('DELETE', url, data, {...config, headers: {'X-CSRFToken': Cookies.get('csrftoken'), ...(config.headers ?? {})}})
  }
}

export default new ApiService()
