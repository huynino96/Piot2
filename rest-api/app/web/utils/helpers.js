import jwt_decode from 'jwt-decode';

const redirectBasedOnRole = (router) => {
    if (typeof window !== 'undefined') {
        const accessToken = window.localStorage.getItem('access_token');
        if (accessToken) {
            const userData = jwt_decode(accessToken);
            const { userName } = userData;
            if (userName) {
                if (userName.indexOf('admin') > -1) {
                    router.push('/admin');
                } else if (userName.indexOf('manager') > -1) {
                    router.push('/manager');
                } else {
                    router.push('/user');
                }
            }
        }
    }
};

const isRole = name => {
    if (typeof window === 'undefined') {
        return false;
    }
    const accessToken = window.localStorage.getItem('access_token');
    if (!accessToken) {
        return false;
    }
    const userData = jwt_decode(accessToken);
    const { userName } = userData;
    if (userName) {
        if (userName.indexOf('admin') > -1 && name === 'admin') {
            return true;
        } else if (userName.indexOf('manager') > -1 && name === 'manager') {
            return true;
        } else if (userName.indexOf('admin') < 0 && userName.indexOf('manager') < 0 &&name === 'user') {
            return true;
        }
    }
    return false;
};

const isAuthenticate = () => {
    if (typeof window === 'undefined') {
        return false;
    }
    return window.localStorage.getItem('access_token') !== null;
};

export {
    redirectBasedOnRole,
    isRole,
    isAuthenticate
}
