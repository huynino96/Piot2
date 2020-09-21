import { Button, Form, FormGroup, Input, Label } from 'reactstrap';
import { useForm } from 'react-hook-form';

const Login = () => {
    const { handleSubmit, register, errors } = useForm();
    const onSubmit = values => console.log(values);

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
