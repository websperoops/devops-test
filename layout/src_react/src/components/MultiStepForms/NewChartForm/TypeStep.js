import React, { useState, useEffect } from 'react'

const TypeStep = ({ charts, handleSetChart, handleNextbtn, chartimgs }) => {

    const [chosenChart, setChosenChart] = useState()

    const handleChartChange = (chart) => {
        setChosenChart(chart)
        handleSetChart(chart)
        handleNextbtn(true)

    }

    useEffect(() => {
        handleNextbtn(false)
    }, [])


    return (
        <>
            <h4 style={{ opacity: '0.8' }}>Select metric type</h4>

            <div className="d-flex flex-row mt-4 flex-wrap justify-content-center type_item_container">
                {charts && charts.map(chart => {
                    const index = chartimgs.findIndex(c => c.chart == chart);
                    let imgPath = null
                    if (index > -1) {
                        imgPath = chartimgs[index].img
                    }

                    console.log(chart)
                    return (
                        <div key={chart} onClick={() => handleChartChange(chart)} className={"account_item d-fex flex-column justify-content-center align-items-center " + (chosenChart == chart ? 'border-yellow' : '')}>
                            <img className='mx-auto' width={35} height={35} src={`${imgPath}`} />
                            <p className="text-capialize mt-2">{chart.replace(/_/g, ' ')}</p>
                        </div>
                    )
                })}
            </div>
        </>
    )

}

export default TypeStep;