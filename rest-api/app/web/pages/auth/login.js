import {useContext, useEffect} from 'react';
import { Button, Form, FormGroup, Input, Label } from 'reactstrap';
import { useForm } from 'react-hook-form';
import { NotificationManager } from 'react-notifications';
import { useRouter } from 'next/router';
import api from '../../api';
import AppContext from '../../context/AppContext';
import { redirectBasedOnRole } from '../../utils/helpers';

const Login = () => {
    const { handleSubmit, register, errors } = useForm();
    const { authenticated, setAuthenticated } = useContext(AppContext);
    const router = useRouter();

    useEffect(() => {
        if (authenticated) {
            redirectBasedOnRole(router);
        }
    }, [authenticated]);

    const onSubmit = async values => {
        try {
            const { access_token } = await api.post('/auth/login', values);
            window.localStorage.setItem('access_token', access_token);
            setAuthenticated(true);
        } catch (e) {
            NotificationManager.error('Can not login');
            setAuthenticated(false);
        }
    };

    return (
        <Form onSubmit={handleSubmit(onSubmit)}>
            <FormGroup>
                <Label for="username">Username</Label>
                <Input
                    type="username"
                    name="username"
                    placeholder="Enter username"
                    innerRef={register({ required: true })}
                />
                {errors.username && errors.username.message}
            </FormGroup>
            <FormGroup>
                <Label for="password">Password</Label>
                <Input
                    type="password"
                    name="password"
                    placeholder="Enter password"
                    innerRef={register({ required: true })}
                />
                {errors.password && errors.password.message}
            </FormGroup>
            <Button type="submit">Submit</Button>
        </Form>
    );
};

export default Login;
