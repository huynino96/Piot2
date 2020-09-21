import { useEffect, useContext } from 'react';
import { useRouter } from 'next/router';
import AppContext from '../context/AppContext';

const Home = () => {
    const { authenticated } = useContext(AppContext);
    const router = useRouter();

    useEffect(() => {
        if (authenticated) {
            router.push('/user');
        } else {
            router.push('/auth/login');
        }
    }, []);

    return <></>;
};

export default Home;
