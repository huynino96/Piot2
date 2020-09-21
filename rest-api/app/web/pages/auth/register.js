import { Button, Form, FormGroup, Input, Label } from 'reactstrap';
import { useForm } from 'react-hook-form';

const Register = () => {
    const { handleSubmit, register, errors } = useForm();
    const onSubmit = values => console.log(values);

    return (
        <Form onSubmit={handleSubmit(onSubmit)}>
            <FormGroup>
                <Label for="first_name">First Name</Label>
                <Input
                    type="text"
                    name="first_name"
                    placeholder="Enter first name"
                    innerRef={register({ required: true })}
                />
                {errors.first_name && errors.first_name.message}
            </FormGroup>
            <FormGroup>
                <Label for="last_name">Last Name</Label>
                <Input
                    type="text"
                    name="last_name"
                    placeholder="Enter last name"
                    innerRef={register({ required: true })}
                />
                {errors.last_name && errors.last_name.message}
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

export default Register;
