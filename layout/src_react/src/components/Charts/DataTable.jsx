import React,{useEffect,useState} from 'react'
import DataTable from 'react-data-table-component';

const Table = ({data, id}) => {
    const [columns,  setColumns] = useState([])

    useEffect(() => {
        if(data) {
            document.querySelector(`#${id}_menu h5`).textContent = data.title // TODO: Pass Title down to parent component so it could get set by the parent.
           var cols = []

           data.columns.map(col => {
               cols.push({name: col, selector: col , sortable: true, allowOverflow: false,})
           })
        
        setColumns(cols)

        }
    },[data])
    return (
        <DataTable 
        noHeader={true}
        responsive={true}
        overflowY={true}
        columns={columns}
        striped={true}
        data={data.series}
        />
    )
}

export default Table;