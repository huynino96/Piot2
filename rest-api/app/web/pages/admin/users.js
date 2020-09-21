import { useState, useEffect } from 'react';
import MaterialTable from 'material-table';
import api from '../../api';

const Users = () => {
    const [data, setData] = useState([]);
    const [iserror, setIserror] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {
        api.get("/users")
            .then(res => {
                setData(res.data.data)
            })
            .catch(error=>{
                setErrorMessage(["Cannot load user data"])
                setIserror(true)
            });
    }, []);

    const handleRowAdd = (newData, resolve) => {
        //validation
        let errorList = []
        if(newData.first_name === undefined){
            errorList.push("Please enter first name")
        }
        if(newData.last_name === undefined){
            errorList.push("Please enter last name")
        }
        if(newData.email === undefined || validateEmail(newData.email) === false){
            errorList.push("Please enter a valid email")
        }
        if(errorList.length < 1){ //no error
            api.post("/users", newData)
                .then(res => {
                    let dataToAdd = [...data];
                    dataToAdd.push(newData);
                    setData(dataToAdd);
                    resolve()
                    setErrorMessages([])
                    setIserror(false)
                })
                .catch(error => {
                    setErrorMessages(["Cannot add data. Server error!"])
                    setIserror(true)
                    resolve()
                })
        }else{
            setErrorMessages(errorList)
            setIserror(true)
            resolve()
        }
    };

    const handleRowUpdate = (newData, oldData, resolve) => {
        if (errorList.length < 1) {
            api.patch("/users/"+newData.id, newData)
                .then(res => {
                    const dataUpdate = [...data];
                    const index = oldData.tableData.id;
                    dataUpdate[index] = newData;
                    setData([...dataUpdate]);
                    resolve()
                    setIserror(false)
                    setErrorMessages([])
                })
                .catch(error => {
                    setErrorMessages(["Update failed! Server error"])
                    setIserror(true)
                    resolve()
                })
        }else{
            setErrorMessages(errorList)
            setIserror(true)
            resolve()
        }
    };

    const handleRowDelete = (oldData, resolve) => {
        api.delete("/users/"+oldData.id)
            .then(res => {
                const dataDelete = [...data];
                const index = oldData.tableData.id;
                dataDelete.splice(index, 1);
                setData([...dataDelete]);
                resolve()
            })
            .catch(error => {
                setErrorMessages(["Delete failed! Server error"])
                setIserror(true)
                resolve()
            })
    };

    const columns = [
        {title: "id", field: "id", hidden: true},
        {title: "Email", field: "email"},
    ];

    return (
        <MaterialTable
            title="List of User"
            columns={columns}
            data={data}
            editable={{
                onRowUpdate: (newData, oldData) =>
                    new Promise((resolve) => {
                        handleRowUpdate(newData, oldData, resolve);
                    }),
                onRowAdd: (newData) =>
                    new Promise((resolve) => {
                        handleRowAdd(newData, resolve)
                    }),
                onRowDelete: (oldData) =>
                    new Promise((resolve) => {
                        handleRowDelete(oldData, resolve)
                    }),
            }}
        />
    );
}

export default Users;
