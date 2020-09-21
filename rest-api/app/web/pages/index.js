import { useEffect, useContext } from 'react';
import { useRouter } from 'next/router';
import AppContext from '../context/AppContext';
import { redirectBasedOnRole } from '../utils/helpers';

const Home = () => {
    const { authenticated } = useContext(AppContext);
    const router = useRouter();

    useEffect(() => {
        if (authenticated) {
            redirectBasedOnRole(router);
        } else {
            router.push('/auth/login');
        }
    }, []);

    return <></>;
};

export default Home;
