import React, { useEffect, useState } from 'react'

const DataStep = ({ values, handleValueChange, handleNextbtn }) => {


    const [available, setAvailable] = useState(true)

    const handleChange = (e) => {

        handleValueChange(e.target.value)
        handleNextbtn(true)

    }
    useEffect(() => {
        handleNextbtn(false)
        if (values.length === 0) { //if no values than enable next btn
            handleNextbtn(true)
        }
        else if (values.length == 1 && values[0] == 'N/A') {
            setAvailable(false)
            handleValueChange('N/A')
            handleNextbtn(true)
        }
    }, [])




    return (
        <>
            <h4 style={{ opacity: '0.8' }}>What information do you wish to see?</h4>
            <div>
                <select onChange={(e) => handleChange(e)} style={{ width: '300px' }} disabled={!available}>
                    {available ? <option>Select a data option:</option> : <option>N/A</option>}
                    {values.map(val => <option key={val} value={val}>{val.replace(/_/g, ' ')}</option>)}
                </select>
            </div>
        </>
    )

}

export default DataStep;