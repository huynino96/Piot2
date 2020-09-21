import { useState, useEffect } from 'react';
import { Container } from 'reactstrap';
import AppContext from '../context/AppContext';
import Header from '../components/Partial/Header';

import '../styles/globals.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'react-notifications/lib/notifications.css';

function MyApp({ Component, pageProps }) {
    const [authenticated, setAuthenticated] = useState(false);

    useEffect(() => {
        const token = window.localStorage.getItem('token');
        setAuthenticated(token !== null);
    }, []);

    return (
        <AppContext.Provider value={{ authenticated, setAuthenticated }}>
            <Header />
            <Container className="mt-5">
                <Component {...pageProps} />
            </Container>
        </AppContext.Provider>
    )
}

export default MyApp
