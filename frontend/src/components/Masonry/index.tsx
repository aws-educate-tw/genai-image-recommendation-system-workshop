import React, { useEffect, useState } from 'react';
import { setStatus, getStatus, getSelectedMode, getImages } from '../../features/ControllSlices';
import { useAppDispatch, useAppSelector } from '../../app/hooks'
import { Share2, MoreHorizontal } from 'lucide-react';

const Masonry = () => {
    const status = useAppSelector(getStatus)
    const selectedMode = useAppSelector(getSelectedMode)
    const images = useAppSelector(getImages)

    return (
        <div className="pt-16 flex">
            <div
            className={`
                h-full transition-all duration-300 ease-in-out
                ${status != 'idle' && selectedMode == 'Image mode' ? 'w-[35%]' : 'w-0'}
            `}
            >
            </div>
            <div className="flex-1 transition-all duration-300 ease-in-out">
            <div className={`${status != 'idle' && selectedMode == 'Image mode' ? 'md:columns-2 lg:columns-3' : 'md:columns-3 lg:columns-4'} columns-2 gap-4 space-y-4`}>
                {images.map((image) => (
                <div 
                    key={image.id} 
                    className="break-inside-avoid group relative mb-4 hover:shadow-lg rounded-lg transition-all duration-300 transform hover:-translate-x-1 hover:-translate-y-1"
                    onClick={() => console.log(image.id)}
                >
                    <img 
                    src={image.base64 !== '' ? image.base64 : image.url} 
                    className="w-full rounded-lg object-cover"
                    />
                    <div className="opacity-0 group-hover:opacity-100 absolute bottom-2 right-2 flex space-x-2">
                    <button className="bg-white p-2 rounded-full shadow-md">
                        <Share2 size={16} />
                    </button>
                    <button className="bg-white p-2 rounded-full shadow-md">
                        <MoreHorizontal size={16} />
                    </button>
                    </div>
                </div>
                ))}
            </div>
            </div>
        </div>
    )
}

export default Masonry
