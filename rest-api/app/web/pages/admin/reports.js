import { useState, useEffect } from 'react';
import MaterialTable from 'material-table';
import { NotificationManager } from 'react-notifications';
import api from '../../api';

const Reports = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const { data } = await api.get('/reports');
            const { reports } = data;
            setData(reports);
        } catch (e) {
            NotificationManager.error('Can not get reports');
        }
    };

    const columns = [
        {title: 'User\'s Email', field: 'user.email'},
        {title: 'Plate Number', field: 'car.plateNumber'},
        {title: 'Make', field: 'car.make'},
        {title: 'Message', field: 'message'},
    ];

    return (
        <MaterialTable
            title="List of Issue"
            columns={columns}
            data={data}
        />
    );
}

export default Reports;
