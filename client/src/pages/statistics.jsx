import { Table } from "antd";
import axios from "axios";
import { useEffect, useState } from "react";

const columns = [
    {
        title: 'Word',
        dataIndex: 'word',
        key: 'word'
    },
    {
        title: 'Count',
        dataIndex: 'count',
        key: 'count'
    }
]

function Statistics() {
    var [data, setData] = useState([])

    useEffect(() => axios.get('/api/statistics')
        .then(rep => setData(rep.data.data)), [])
    return (
        <Table columns={columns} dataSource={data} />
    )
}

export default Statistics;