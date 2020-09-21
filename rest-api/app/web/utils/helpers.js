import jwt_decode from 'jwt-decode';

const redirectBasedOnRole = (router) => {
    const accessToken = window.localStorage.getItem('access_token');
    const userData = jwt_decode(accessToken);
    const userName = userData.userName;
    if (userName.indexOf('admin') > -1) {
        router.push('/admin');
    } else if (userName.indexOf('manager') > -1) {
        router.push('/manager');
    } else {
        router.push('/user');
    }
};

export {
    redirectBasedOnRole,
}
