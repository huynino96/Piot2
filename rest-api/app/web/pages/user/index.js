import { useState, useEffect } from 'react';
import MaterialTable from 'material-table';
import api from '../../api';
import { NotificationManager } from 'react-notifications';

const Index = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const { data } = await api.get('/cars');
            const { cars } = data;
            setData(cars);
        } catch (e) {
            NotificationManager.error('Can not get list of cars');
        }
    };

    const handleBook = (event, rowData) => {

    };

    const columns = [
        {title: "id", field: "id", hidden: true},
        {title: "Plate Number", field: "plateNumber"},
        {title: "Make", field: "make"},
        {title: "Body Type", field: "bodyType"},
        {title: "Color", field: "color"},
        {title: "Seats", field: "seats"},
        {title: "Location", field: "location"},
        {title: "Cost Per Hour", field: "costPerHour"},
    ];

    const actions = [
        {
            icon: 'calendar_today',
            tooltip: 'Book',
            onClick: handleBook,
        }
    ];

    return (
        <MaterialTable
            title="Available Car"
            columns={columns}
            data={data}
            actions={actions}
        />
    );
}

export default Index;
