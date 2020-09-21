import { Button, Form, FormGroup, Input, Label } from 'reactstrap';
import api from '../../api';
import {useForm} from "react-hook-form";

const Issue = () => {
    const { handleSubmit, register, errors } = useForm();
    const onSubmit = values => console.log(values);

    return (
        <Form onSubmit={handleSubmit(onSubmit)}>
            <FormGroup>
                <Label for="issue">Issue</Label>
                <Input
                    type="textarea"
                    name="issue"
                    placeholder="Enter issue"
                    rows={10}
                    innerRef={register({ required: true })}
                />
                {errors.issue && errors.issue.message}
            </FormGroup>
            <Button type="submit">Submit</Button>
        </Form>
    );
};

export default Issue;
