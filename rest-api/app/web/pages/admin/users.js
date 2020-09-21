import { useState, useEffect } from 'react';
import MaterialTable from 'material-table';
import api from '../../api';
import { NotificationManager } from 'react-notifications';

const Users = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetchData();
    }, []);

    const fetchData = async () => {
        try {
            const { data } = await api.get('/users');
            const { users } = data;
            setData(users);
        } catch (e) {
            NotificationManager.error('Error', 'Cannot load user data');
        }
    };

    const handleRowAdd = async (newData) => {
        //validation
        if (newData.firstName === undefined){
            NotificationManager.error('Please enter first name');
            return false;
        }

        if (newData.lastName === undefined){
            NotificationManager.error('Please enter last name');
            return false;
        }

        if (newData.email === undefined){
            NotificationManager.error('Please enter email');
            return false;
        }

        if (newData.userName === undefined) {
            NotificationManager.error('Please enter username');
            return false;
        }

        if (newData.password === undefined) {
            NotificationManager.error('Please enter password');
            return false;
        }

        try {
            const response = await api.post('/users', newData);
            const dataToAdd = [...data, { id: response.id, ...newData }];
            setData(dataToAdd);
        } catch (e) {
            console.log(e);
            NotificationManager.error('Cannot add data. Server error!');
        }
    };

    const handleRowUpdate = async (newData, oldData) => {
        console.log(newData);
        try {
            await api.put(`/users/${newData.userId}`, newData);
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
            await api.delete(`/users/${oldData.userId}`);
            const dataDelete = [...data];
            const index = oldData.tableData.id;
            dataDelete.splice(index, 1);
            setData([...dataDelete]);
        } catch (e) {
            NotificationManager.error('Delete failed! Server error')
        }
    };

    const columns = [
        {title: 'userId', field: 'userId', hidden: true},
        {title: 'First Name', field: 'firstName'},
        {title: 'Last Name', field: 'lastName'},
        {title: 'User Name', field: 'userName'},
        {title: 'Email', field: 'email'},
        {title: 'Password', field: 'password'},
    ];

    return (
        <MaterialTable
            title="List of User"
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

export default Users;
