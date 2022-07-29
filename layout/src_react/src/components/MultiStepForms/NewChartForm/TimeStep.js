import React, { useEffect, useState } from 'react'

const TimeStep = ({ times, handleTimeChange }) => {
    const [allTimeOnly, setAllTimeOnly] = useState(false)
    useEffect(() => {
        if (times.length == 1 && times[0] == 'All_Time') {
            handleTimeChange('All_Time')
            setAllTimeOnly(true)
        }
    }, [])

    const handleChange = e => {
        handleTimeChange(e.target.value)
    }

    return (
        <>
            <h4 style={{ opacity: '0.8' }}>Select a time period</h4>

            <div>
                <select onChange={(e) => handleChange(e)} disabled={allTimeOnly}>
                    {allTimeOnly ? <option>All Time</option> : <option>Times</option>}
                    {times.map(time => <option key={time} value={time}>{time.replace(/_/g, ' ')}</option>)}
                </select>
            </div>
        </>
    )

}

export default TimeStep;