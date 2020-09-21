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
            const { data } = await api.post('/auth/login', values);
            const { access_token } = data;
            window.localStorage.setItem('access_token', access_token);
            setAuthenticated(true);
            redirectBasedOnRole(router);
        } catch (e) {
            NotificationManager.error('Can not login');
            setAuthenticated(false);
        }
    };

    return (
        <Form onSubmit={handleSubmit(onSubmit)}>
            <FormGroup>
                <Label for="userName">Username</Label>
                <Input
                    type="text"
                    name="userName"
                    placeholder="Enter username"
                    innerRef={register({ required: true })}
                />
                {errors.userName && errors.userName.message}
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
