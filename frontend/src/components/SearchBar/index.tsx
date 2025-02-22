import React, { useEffect, useState } from 'react'
import { setStatus, setSelectedMode, getSelectedMode, setQuery, getQuery, setIsSearching, getIsSearching, setImages } from '../../features/ControllSlices';
import { useAppDispatch, useAppSelector } from '../../app/hooks'
import { Search, X } from 'lucide-react';
import { useSearchByTextMutation } from '../../api/SearchSlice';
import toast, { Toaster } from 'react-hot-toast';


const SearchBar = () => {
    const dispatch = useAppDispatch()
    const selectedMode = useAppSelector(getSelectedMode)
    const query = useAppSelector(getQuery)
    const isSearching = useAppSelector(getIsSearching)
    
    const [isFocused, setIsFocused] = useState(false)
    const [searchTerm, setSearchTerm] = useState('');
    const [modeIndex, setModeIndex] = useState(0);

    const [pictureLoading, setPictureLoading] = useState(false);

    const modes = [
        'Text mode', 
        'Image mode', 
        // 'Generate mode'
    ];

    const [
        searchByText,
    ] = useSearchByTextMutation()

    const handleModeToggle = () => {
        setSearchTerm('')
        if (selectedMode === 'Text mode') {
            dispatch(setQuery(''))
        }
        setModeIndex((prevIndex) => (prevIndex + 1) % modes.length);
    };

    const handleSearchKeyDownSubmit = (event: React.KeyboardEvent<HTMLInputElement>) => {
        if (event.key === 'Enter') {
            console.log('User pressed Enter with search:', searchTerm);
            dispatch(setSelectedMode(modes[modeIndex]));
            dispatch(setStatus('idle'))
            setIsFocused(false)
            if (modes[modeIndex] === 'Image mode') {
                setPictureLoading(true)
            } else {
                dispatch(setQuery(searchTerm))
                dispatch(setIsSearching(true))
            }
        }
    };

    const handleQuerySubmit = async () => {
        try {
            const searchResults = await searchByText(query).unwrap()
                        // console.log(searchResults)
            
            const results = searchResults.results;

            const formattedImages = results.map((url: string, index: number) => {    
                return {
                    id: index + 1,
                    url: url,
                };
            });

            dispatch(setImages(formattedImages))

            toast.success('Successfully searched by text! ', {
                position: "bottom-center",
                duration: 2000,
            });
        } catch (SearchError) {
            console.log(SearchError)
            toast.error('Failed to search by text! ', {
                position: "bottom-center",
                duration: 2000,
            });
        }
      }
    

    useEffect(() => {
        const handleAsync = async () => {
            if (query !== '' && selectedMode == 'Text mode' && isSearching) {
                await handleQuerySubmit()
                dispatch(setIsSearching(false))
                dispatch(setStatus('success'))
            }
        }
        handleAsync()
    }, [isSearching])

    const handleImageLoad = () => {
        console.log('Image loaded successfully');
        dispatch(setStatus('preview'))
        dispatch(setQuery(searchTerm))
        setSearchTerm('')
        setPictureLoading(false)
        toast.success('Image loaded successfully! ', {
            position: "bottom-center",
            duration: 2000,
        });
      };
    
    // 當圖片載入失敗時，設定為無效
    const handleImageError = () => {
        console.log('Image failed to load');
        toast.error('Image failed to load! ', {
            position: "top-center",
            duration: 2000,
        });
        setSearchTerm('')
        setPictureLoading(false)
        // console.log('Image failed to load: ', status);
    };
    
    return (
        <div className="fixed left-0 w-[100%] top-0 bg-white p-4 z-50 flex justify-center">
            <Toaster
                reverseOrder={false}
            />
            <button
                disabled={isSearching}
                onClick={handleModeToggle}
                className="relative w-40 h-9 right-4 -translate-y-0 px-2 py-1 rounded-lg border-0 bg-[#ff3856] text-white text-[15px] tracking-wider transition-all duration-300 ease-in-out shadow-[0px_6px_0px_0px_rgb(201,46,70)] hover:shadow-[0px_5px_0px_0px_rgb(201,46,70)] active:bg-[#ff3856] active:shadow-[0px_4px_0px_0px_rgb(201,46,70)] active:translate-y-1 active:transition-[transform] active:duration-200 cursor-pointer "
            >
                {modes[modeIndex]}
            </button>
            <div
            className={`relative rounded-lg transition-all duration-300
                ${isFocused ? 'md:w-[60%] lg:w-[70%]' : 'w-[40%]'}`}
            >
                <input
                    type="text"
                    disabled={isSearching}
                    placeholder="Search"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    onFocus={() => setIsFocused(true)}
                    onBlur={() => setIsFocused(false)}
                    onKeyDown={handleSearchKeyDownSubmit}
                    className={`w-full p-2 pl-10  flex justify-left rounded-lg focus:outline-none bg-gray-100`}
                />
                <Search
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
                    size={20}
                />
                {!isFocused && query !== '' && modes[modeIndex] === 'Text mode' ? 
                <button 
                    className={`absolute p-2 right-0 top-1/2 -translate-y-1/2 text-gray-400 rounded-lg hover:bg-gray-200 transition-all duration-300 ease-in-out`}
                    onClick={() => {
                        dispatch(setQuery(''))
                        setSearchTerm('')
                    }}
                > <X size={20} />
                </button> : null}
            </div>
            {pictureLoading ? <img
                src={searchTerm}
                alt="預覽圖片"
                className="fixed w-1 h-auto opacity-0"
                onLoad={handleImageLoad}   // 圖片載入成功
                onError={handleImageError} // 圖片載入失敗
            /> : null}
        </div>
    )
}

export default SearchBar
