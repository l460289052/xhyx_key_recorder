import { Checkbox, Row, Col, Divider } from "antd"
import axios from "axios"
import { useEffect, useState } from "react"

function Analysis() {
    const [options, setOptions] = useState([])
    const [checkedList, setCheckedList] = useState([])

    useEffect(() => {
        axios.get("/api/get_records")
            .then(rep => setOptions(rep.data.data))
    }, [])

    return (
        <>
            <Checkbox.Group options={options} value={checkedList} onChange={list => setCheckedList(list)} />
            <Divider />
            <Checkbox
                indeterminate={checkedList.length > 0 && checkedList.length < options.length}
                checked={checkedList.length === options.length}
                onChange={e => setCheckedList(e.target.checked ? options : [])}>选择全部文件</Checkbox>
        </>
    )
}

export default Analysis