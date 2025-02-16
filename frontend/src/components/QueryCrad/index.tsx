import React, { useEffect} from 'react'
import { setStatus, getStatus, getSelectedMode, getQuery, getIsSearching, setIsSearching, setImages } from '../../features/ControllSlices';
import { useAppDispatch, useAppSelector } from '../../app/hooks'
import { Search } from 'lucide-react';
import { useSearchByImageMutation } from '../../api/SearchSlice';
import toast, { Toaster } from 'react-hot-toast';
import axios from 'axios';

const QueryCard = () => {
    const dispatch = useAppDispatch()
    const status = useAppSelector(getStatus)
    const selectedMode = useAppSelector(getSelectedMode)
    const query = useAppSelector(getQuery)
    const isSearching = useAppSelector(getIsSearching)

    const [
            searchByImage,
            {
              isLoading: querySearchLoading,
              isSuccess: querySearchSuccess,
              error: querySearchError,
            },
    ] = useSearchByImageMutation()

    const handleSearchSubmit = () => {
        dispatch(setIsSearching(true))
    }

    const handleQuerySubmit = async () => {
        try {
            const searchResults = await searchByImage(query).unwrap()
            // console.log(searchResults)

            const results = searchResults.results;
            const images = searchResults.images;

            const formattedImages = results.map((url: string, index: number) => {
                const filename = url.split('amazonaws.com/').pop(); // 取得網址最後的檔名
                if (!filename) return null;
                const base64 = images[filename] || ''; // 從 images 物件中取得對應的 base64
    
                return {
                    id: index + 1,
                    url: url,
                    base64: 'data:image/jpeg;base64,' + base64,
                };
            });

            dispatch(setImages(formattedImages))
            // 先計時 3 秒
            // await new Promise(resolve => setTimeout(resolve, 3000))

            toast.success('Successfully searched by image!', {
                position: "bottom-center",
                duration: 2000,
            });
        } catch (SearchError) {
            console.log(SearchError)
            toast.error('Failed to search by image!', {
                position: "bottom-center",
                duration: 2000,
            });
        }
    }

    useEffect(() => {
        const handleAsync = async () => {
            if (query !== '' && selectedMode == 'Image mode' && isSearching) {
                await handleQuerySubmit()
                dispatch(setIsSearching(false))
                dispatch(setStatus('success'))
            }
        }
        handleAsync()
    }, [isSearching])

    return (
        <div className={`fixed top-20 left-0 h-[90%] px-4 z-40 transition-all duration-300 ease-in-out ${status != 'idle' && selectedMode == 'Image mode' ? 'w-[35%] opacity-100' : 'w-0 opacity-0'}`}>
            <Toaster
                reverseOrder={false}
            />
            <div className="flex bg-white rounded-lg shadow-lg w-full h-full mb-4 justify-center items-center p-[10%] border-1 border-gray-300 flex-col space-y-8">
                <img
                        src={query}
                        alt="預覽圖片"
                        className="max-w-[100%] max-h-[80%] rounded-lg object-cover shadow-lg border-3 border-white"
                />
                <button
                    disabled={isSearching}
                    onClick={handleSearchSubmit}
                    className={`
                    relative w-[150px] border-[#ff3856] border-1 bg-none text-[#ff3856]
                    px-4 py-2 font-bold uppercase tracking-wide 
                    transition-opacity duration-200 rounded-md
                    shadow-[0px_5px_2px_#ff3856]
                    active:top-[4px] active:shadow-[0px_3px_2px_#ff3856] ${isSearching ? 'opacity-50' : 'opacity-100'}`}
                >
                    <p>Search!</p>
                </button>
                
            </div>
        </div>
    )
}

export default QueryCard
