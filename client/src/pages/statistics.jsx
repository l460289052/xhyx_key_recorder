import { Table } from "antd";
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

    useEffect(() => fetch('/api/statistics')
        .then(rep => rep.json())
        .then(rep => setData(rep.data)), [])
    return (
        <Table columns={columns} dataSource={data} />
    )
}

export default Statistics;