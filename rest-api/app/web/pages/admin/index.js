import { useState, useEffect } from 'react';
import MaterialTable from 'material-table';
import { NotificationManager } from 'react-notifications';
import api from '../../api';

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
            NotificationManager.error('Error', 'Cannot load cars data');
        }
    };

    const handleRowAdd = async (newData) => {
        //validation
        if (newData.plateNumber === undefined){
            NotificationManager.error('Please enter plate number');
            return false;
        }

        if (newData.make === undefined){
            NotificationManager.error('Please enter make');
            return false;
        }

        if (newData.bodyType === undefined){
            NotificationManager.error('Please enter body type');
            return false;
        }

        if (newData.color === undefined) {
            NotificationManager.error('Please enter color');
            return false;
        }

        if (newData.seats === undefined) {
            NotificationManager.error('Please enter seats');
            return false;
        }

        if (newData.location === undefined) {
            NotificationManager.error('Please enter location');
            return false;
        }

        if (newData.costPerHour === undefined) {
            NotificationManager.error('Please enter costPerHour');
            return false;
        }

        try {
            const response = await api.post('/cars', newData);
            const dataToAdd = [...data, { id: response.id, ...newData }];
            setData(dataToAdd);
        } catch (e) {
            NotificationManager.error('Cannot add data. Server error!');
        }
    };

    const handleRowUpdate = async (newData, oldData) => {
        try {
            await api.put(`/cars/${newData.carId}`, newData);
            const dataUpdate = [...data];
            const index = oldData.tableData.id;
            dataUpdate[index] = newData;
            setData([...dataUpdate]);
        } catch (e) {
            NotificationManager.error('Update failed! Server error');
        }
    };

    const handleRowDelete = async (oldData) => {
        try {
            await api.delete(`/cars/${oldData.carId}`);
            const dataDelete = [...data];
            const index = oldData.tableData.id;
            dataDelete.splice(index, 1);
            setData([...dataDelete]);
        } catch (e) {
            NotificationManager.error('Delete failed! Server error')
        }
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

    return (
        <MaterialTable
            title="List of Car"
            columns={columns}
            data={data}
            editable={{
                onRowUpdate: async (newData, oldData) => await handleRowUpdate(newData, oldData),
                onRowAdd: async newData => await handleRowAdd(newData),
                onRowDelete: async oldData => await handleRowDelete(oldData),
            }}
        />
    );
}

export default Index;
