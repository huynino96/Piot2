import { useState, useEffect } from 'react';
import { NotificationManager } from 'react-notifications';
import MaterialTable from 'material-table';
import api from '../../api';

const Histories = () => {
    const [data, setData] = useState([]);

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

    const handleReturn = async (event, rowData) => {
        try {
            const { car } = rowData;
            const { carId } = car;
            await api.post(`/return_car/${carId}`);
            setData(data.filter(item => item.car.carId !== carId));
            NotificationManager.success('Returned successfully');
        } catch (e) {
            NotificationManager.error('Can not return car');
        }
    };

    const columns = [
        {title: 'carId', field: 'car.carId', hidden: true},
        {title: 'Rented Date', field: 'rentedDate'},
        {title: 'Returned Date', field: 'returnedDate'},
        {title: 'Plate Number', field: 'car.plateNumber'},
        {title: 'Make', field: 'car.make'},
        {title: 'Body Type', field: 'car.bodyType'},
        {title: 'Color', field: 'car.color'},
        {title: 'Seats', field: 'car.seats'},
        {title: 'Location', field: 'car.location'},
        {title: 'Cost Per Hour', field: 'car.costPerHour'},
    ];

    const actions = [
        {
            icon: 'keyboard_return',
            tooltip: 'Return',
            onClick: handleReturn,
        }
    ];

    return (
        <MaterialTable
            title="Booked Car"
            columns={columns}
            data={data}
            actions={actions}
        />
    );
};

export default Histories;
