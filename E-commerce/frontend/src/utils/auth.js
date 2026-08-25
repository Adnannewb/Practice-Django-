export const saveToken=(token)=>{
    if (token?.access) {
        localStorage.setItem('access_token',token.access);
    }
    if (token?.refresh) {
        localStorage.setItem('refresh_token',token.refresh);
    }
};
export const clearToken=()=>{
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
};

export const getAccessToken=()=>{
    return localStorage.getItem('access_token');
};

export const authFetch=(url,options={})=>{  
    const token=getAccessToken();
    const headers=new Headers(options.headers || {});
    if (token) {
        headers.set('Authorization',`Bearer ${token}`);
    }
    if (options.body && !(options.body instanceof FormData) && !headers.has('Content-Type')) {
        headers.set('Content-Type','application/json');
    }
    return fetch(url,{...options,headers});
};