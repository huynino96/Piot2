import { useEffect } from 'react';
import { Button, Form, FormGroup, Input, Label } from 'reactstrap';
import { useForm } from 'react-hook-form';
import { NotificationManager } from 'react-notifications';
import { useRouter } from 'next/router';
import api from '../../api';
import { redirectBasedOnRole, isAuthenticate } from '../../utils/helpers';

const Login = () => {
    const { handleSubmit, register, errors } = useForm();
    const router = useRouter();

    useEffect(() => {
        if (isAuthenticate()) {
            redirectBasedOnRole(router);
        }
    }, [isAuthenticate()]);

    const onSubmit = async values => {
        try {
            const { data } = await api.post('/auth/login', values);
            const { access_token } = data;
            window.localStorage.setItem('access_token', access_token);
            redirectBasedOnRole(router);
        } catch (e) {
            NotificationManager.error('Can not login');
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
