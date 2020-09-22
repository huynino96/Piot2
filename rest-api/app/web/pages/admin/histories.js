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
            const { data } = await api.get('/booked_cars');
            const { bookedCars } = data;
            setData(bookedCars);
        } catch (e) {
            NotificationManager.error('Can not get booked cars');
        }
    };

    const columns = [
        {title: 'User\'s Email', field: 'user.email'},
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

    return (
        <MaterialTable
            title="Car Rental History"
            columns={columns}
            data={data}
        />
    );
}

export default Histories;
