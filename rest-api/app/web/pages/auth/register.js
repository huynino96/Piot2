import { useContext, useEffect } from 'react';
import { Button, Form, FormGroup, Input, Label } from 'reactstrap';
import { useForm } from 'react-hook-form';
import { NotificationManager } from 'react-notifications';
import { useRouter } from 'next/router';
import api from '../../api';
import { isAuthenticate, redirectBasedOnRole } from '../../utils/helpers';

const Register = () => {
    const { handleSubmit, register, errors } = useForm();
    const router = useRouter();

    useEffect(() => {
        if (isAuthenticate()) {
            redirectBasedOnRole(router);
        }
    }, []);

    const onSubmit = async values => {
        try {
            const { data } = await api.post('/auth/register', values);
            const { access_token } = data;
            window.localStorage.setItem('access_token', access_token);
            redirectBasedOnRole(router);
        } catch (e) {
            NotificationManager.error('Can not register');
        }
    };

    return (
        <Form onSubmit={handleSubmit(onSubmit)}>
            <FormGroup>
                <Label for="first_name">First Name</Label>
                <Input
                    type="text"
                    name="firstName"
                    placeholder="Enter first name"
                    innerRef={register({ required: true })}
                />
                {errors.firstName && errors.firstName.message}
            </FormGroup>
            <FormGroup>
                <Label for="last_name">Last Name</Label>
                <Input
                    type="text"
                    name="lastName"
                    placeholder="Enter last name"
                    innerRef={register({ required: true })}
                />
                {errors.lastName && errors.lastName.message}
            </FormGroup>
            <FormGroup>
                <Label for="email">Email</Label>
                <Input
                    type="email"
                    name="email"
                    placeholder="Enter email"
                    innerRef={register({
                        required: "Required",
                        pattern: {
                            value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                            message: "invalid email address"
                        }
                    })}
                />
                {errors.email && errors.email.message}
            </FormGroup>
            <FormGroup>
                <Label for="username">Username</Label>
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

export default Register;
