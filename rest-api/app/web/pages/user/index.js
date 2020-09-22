import { useState, useEffect } from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter, Form, FormGroup, Label, Input } from 'reactstrap';
import MaterialTable from 'material-table';
import { useForm } from 'react-hook-form';
import api from '../../api';
import { NotificationManager } from 'react-notifications';

const Index = () => {
    const { handleSubmit, register, errors } = useForm();
    const [modal, setModal] = useState(false);
    const [data, setData] = useState([]);
    const [rowData, setRowData] = useState({});

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const { data } = await api.get('/cars');
            const { cars } = data;
            setData(cars.filter(item => !item.is_booked));
        } catch (e) {
            NotificationManager.error('Can not get list of cars');
        }
    };

    const toggle = () => setModal(!modal);

    const onSubmit = async values => {
        try {
            const { carId } = rowData;
            await api.post(`/book_car/${carId}`, values);
            setData(data.filter(item => item.carId !== carId));
            NotificationManager.success('Book successfully');
            toggle();
        } catch (e) {
            NotificationManager.error('Can not book car');
        }
    };

    const handleBook = (event, rowData) => {
        toggle();
        setRowData(rowData);
    };

    const columns = [
        {title: 'carId', field: 'carId', hidden: true},
        {title: 'Plate Number', field: 'plateNumber'},
        {title: 'Make', field: 'make'},
        {title: 'Body Type', field: 'bodyType'},
        {title: 'Color', field: 'color'},
        {title: 'Seats', field: 'seats'},
        {title: 'Location', field: 'location'},
        {title: 'Cost Per Hour', field: 'costPerHour'},
    ];

    const actions = [
        {
            icon: 'calendar_today',
            tooltip: 'Book',
            onClick: handleBook,
        }
    ];

    return (
        <>
            <MaterialTable
                title="Available Car"
                columns={columns}
                data={data}
                actions={actions}
            />
            <Modal isOpen={modal} toggle={toggle}>
                <Form onSubmit={handleSubmit(onSubmit)}>
                    <ModalHeader toggle={toggle}>Book Car</ModalHeader>
                    <ModalBody>
                        <FormGroup>
                            <Label for="rentedDate">Rented Date</Label>
                            <Input
                                type="text"
                                name="rentedDate"
                                placeholder="Enter rented date"
                                innerRef={register({ required: true })}
                            />
                            {errors.rentedDate && errors.rentedDate.message}
                        </FormGroup>
                        <FormGroup>
                            <Label for="returnedDate">Returned Date</Label>
                            <Input
                                type="text"
                                name="returnedDate"
                                placeholder="Enter returned date"
                                innerRef={register({ required: true })}
                            />
                            {errors.returnedDate && errors.returnedDate.message}
                        </FormGroup>
                    </ModalBody>
                    <ModalFooter>
                        <Button color="primary" type="submit">Submit</Button>{' '}
                        <Button color="secondary" onClick={toggle}>Cancel</Button>
                    </ModalFooter>
                </Form>
            </Modal>
        </>
    );
};

export default Index;
