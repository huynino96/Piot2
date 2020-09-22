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

    const columns = [
        {title: "Rented Date", field: "rentedDate"},
        {title: "Returned Date", field: "returnedDate"},
        {title: "Plate Number", field: "plateNumber"},
        {title: "Make", field: "make"},
        {title: "Body Type", field: "body_type"},
        {title: "Color", field: "color"},
        {title: "Seats", field: "seats"},
        {title: "Location", field: "location"},
        {title: "Cost Per Hour", field: "cost_per_hour"},
    ];

    return (
        <MaterialTable
            title="Booked Car"
            columns={columns}
            data={data}
        />
    );
};

export default Histories;
