import { useEffect, useState } from 'react';
import { NotificationManager } from 'react-notifications';
import { Button, Form, FormGroup, Input, Label } from 'reactstrap';
import api from '../../api';
import { useForm } from 'react-hook-form';

const Issue = () => {
    const [data, setData] = useState([]);
    const { handleSubmit, register, errors } = useForm();

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const { data } = await api.get('/booked_cars/me');
            const { bookedCars } = data;
            setData(bookedCars);
        } catch (e) {
            NotificationManager.error('Can not get booked cars');
        }
    };

    const onSubmit = async (values) => {
        try {
            await api.post('/reports', values);
            NotificationManager.success('Sent successfully');
        } catch (e) {
            NotificationManager.error('Can not send issue');
        }
    };

    return (
        <Form onSubmit={handleSubmit(onSubmit)}>
            <FormGroup>
                <Label for="car">Car</Label>
                <Input
                    type="select"
                    name="carId"
                    innerRef={register({ required: true })}
                >
                    {data.map(item => (
                        <option value={item.car.carId}>
                            {item.car.plateNumber} | {item.car.make}
                        </option>
                    ))}
                </Input>
                {errors.message && errors.message.message}
            </FormGroup>
            <FormGroup>
                <Label for="issue">Message</Label>
                <Input
                    type="textarea"
                    name="message"
                    placeholder="Enter message"
                    rows={10}
                    innerRef={register({ required: true })}
                />
                {errors.message && errors.message.message}
            </FormGroup>
            <Button type="submit">Submit</Button>
        </Form>
    );
};

export default Issue;
