import { Container } from 'reactstrap';
import Header from '../components/Partial/Header';
import { NotificationContainer } from 'react-notifications';

import '../styles/globals.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'react-notifications/lib/notifications.css';

function MyApp({ Component, pageProps }) {
    return (
        <>
            <Header />
            <Container className="mt-5">
                <Component {...pageProps} />
            </Container>
            <NotificationContainer />
        </>
    )
}

export default MyApp
