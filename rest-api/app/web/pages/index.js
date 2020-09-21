import { useEffect, useContext } from 'react';
import { useRouter } from 'next/router';
import { redirectBasedOnRole, isAuthenticate } from '../utils/helpers';

const Home = () => {
    const router = useRouter();

    useEffect(() => {
        if (isAuthenticate()) {
            redirectBasedOnRole(router);
        } else {
            router.push('/auth/login');
        }
    }, []);

    return <></>;
};

export default Home;
