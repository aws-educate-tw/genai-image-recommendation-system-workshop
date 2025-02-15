import React from 'react'
import { DotLoader } from 'react-spinners';
import { useAppSelector } from '../../app/hooks';
import { getIsSearching, getStatus, getSelectedMode } from '../../features/ControllSlices';

const Loader = () => {
    const isSearching = useAppSelector(getIsSearching)
    const status = useAppSelector(getStatus)
    const selectedMode = useAppSelector(getSelectedMode)

    return (
        isSearching ? 
        <div className={`absolute fixed mt-16 top-0 right-0 bg-white opacity-80 flex ${selectedMode == 'Image mode' ? 'w-[65%]' : 'w-full'} h-screen justify-center items-center z-100`}>  
            <DotLoader color="red" className="opacity-100"/>
        </div> : null
    )
}

export default Loader
