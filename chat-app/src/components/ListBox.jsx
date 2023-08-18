import { useState, useEffect} from 'react';

export const ListBox = (props) => {

     useEffect(
        () => {}, [props.input]
     )

    return (

        <div >
            {
                props.input?.map((item, index) => (
                    <p key={index}> {item} </p>
                ))
            }
        </div>
    )
}

