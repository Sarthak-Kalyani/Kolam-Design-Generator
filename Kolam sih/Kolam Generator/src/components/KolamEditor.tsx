// 'use client';

// import { KolamPattern } from '@/types/kolam';
// import { KolamExporter } from '@/utils/kolamExporter';
// import { KolamGenerator } from '@/utils/kolamGenerator';
// import { durationToSpeed, generateEmbedURL, speedToDuration, updateURL, useKolamURLParams } from '@/utils/urlParams';
// import React, { useCallback, useEffect, useRef, useState } from 'react';
// import { KolamDisplay } from './KolamDisplay';

// export const KolamEditor: React.FC = () => {
// 	const [currentPattern, setCurrentPattern] = useState<KolamPattern | null>(null);
// 	const [isExporting, setIsExporting] = useState(false);
// 	const [showDownloadMenu, setShowDownloadMenu] = useState(false);
// 	const [animationState, setAnimationState] = useState<'stopped' | 'playing' | 'paused'>('stopped');
// 	const kolamRef = useRef<HTMLDivElement>(null);

// 	const urlParams = useKolamURLParams();
// 	const [size, setSize] = useState(urlParams.size);
// 	const [animationSpeed, setAnimationSpeed] = useState(durationToSpeed(urlParams.duration));
// 	const [animationDuration, setAnimationDuration] = useState(urlParams.duration);
// 	const [initialAutoAnimate, setInitialAutoAnimate] = useState(urlParams.initialAutoAnimate);

// 	useEffect(() => {
// 		updateURL({ size, duration: animationDuration, initialAutoAnimate });
// 	}, [size, animationDuration, initialAutoAnimate]);

// 	useEffect(() => {
// 		const newDuration = speedToDuration(animationSpeed);
// 		setAnimationDuration(newDuration);
// 	}, [animationSpeed]);

// 	useEffect(() => {
// 		const handleClickOutside = (event: MouseEvent) => {
// 			if (showDownloadMenu && !(event.target as Element).closest('.download-menu')) {
// 				setShowDownloadMenu(false);
// 			}
// 		};
// 		document.addEventListener('mousedown', handleClickOutside);
// 		return () => document.removeEventListener('mousedown', handleClickOutside);
// 	}, [showDownloadMenu]);

// 	useEffect(() => {
// 		if (animationState === 'playing' && currentPattern) {
// 			const timer = setTimeout(() => {
// 				setAnimationState('stopped');
// 			}, animationDuration);
// 			return () => clearTimeout(timer);
// 		}
// 	}, [animationState, currentPattern, animationDuration]);

// 	const getAnimationTiming = (speed: number) => {
// 		return speedToDuration(speed);
// 	};

// 	const generatePattern = useCallback(() => {
// 		console.log('🎯 Generating kolam pattern');
// 		try {
// 			const pattern = KolamGenerator.generateKolam1D(size);
// 			setCurrentPattern(pattern);
// 			setAnimationState('stopped');

// 			if (initialAutoAnimate) {
// 				setTimeout(() => setAnimationState('playing'), 100);
// 			}
// 		} catch (error) {
// 			const errorMessage = error instanceof Error ? error.message : String(error);
// 			alert(`Error generating pattern: ${errorMessage}`);
// 		}
// 	}, [size, initialAutoAnimate]);

// 	useEffect(() => {
// 		generatePattern();
// 	}, [generatePattern]);

// 	const exportPattern = async (format: 'svg' | 'png' | 'gif') => {
// 		if (!currentPattern || !kolamRef.current) return;
// 		setIsExporting(true);
// 		try {
// 			switch (format) {
// 				case 'svg':
// 					await KolamExporter.downloadSVG(currentPattern);
// 					break;
// 				case 'png':
// 					await KolamExporter.downloadPNG(kolamRef.current, currentPattern.name);
// 					break;
// 				case 'gif':
// 					await KolamExporter.downloadAnimatedGIF(
// 						kolamRef.current,
// 						currentPattern,
// 						currentPattern.name,
// 						{ format: 'gif', frameCount: 30, delay: animationDuration }
// 					);
// 					break;
// 			}
// 		} catch (error) {
// 			alert('Export failed. Please try again.');
// 		} finally {
// 			setIsExporting(false);
// 		}
// 	};

// 	const getEmbedCode = async () => {
// 		if (!currentPattern) return;
// 		try {
// 			const embedURL = generateEmbedURL({ size, background: '#1e1e2f', brush: '#00FFFF' });
// 			const embedCode = `<img src="${embedURL}" alt="Kolam Pattern" style="max-width: 100%; height: auto;" />`;
// 			await navigator.clipboard.writeText(embedCode);
// 			alert('Embed code copied to clipboard!');
// 		} catch (error) {
// 			alert('Failed to copy embed code.');
// 		}
// 	};

// 	const copyRawSVG = async () => {
// 		if (!currentPattern) return;
// 		try {
// 			const svgContent = await KolamExporter.exportAsSVG(currentPattern);
// 			await navigator.clipboard.writeText(svgContent);
// 			alert('Raw SVG code copied to clipboard!');
// 		} catch (error) {
// 			alert('Failed to copy raw SVG.');
// 		}
// 	};

// 	return (
// 		<div className="kolam-editor bg-[#1e1e2f] text-white min-h-screen">
// 			{/* Header */}
// 			<header className="p-6" style={{ backgroundColor: '#5ba293' }}>
// 				<div className="max-w-6xl mx-auto">
// 					<h1 className="text-4xl font-bold text-center tracking-wide">Kolam Generator</h1>
// 					<p className="text-center mt-2 text-lg opacity-90">
// 						Generate beautiful traditional South Indian Kolam patterns
// 					</p>
// 				</div>
// 			</header>

// 			<div className="max-w-6xl mx-auto p-8">
// 				{/* Display Area */}
// 				<div className="kolam-display-area">
// 					{currentPattern ? (
// 						<div
// 							ref={kolamRef}
// 							className="kolam-container relative flex justify-center items-center bg-[#2e2e3f] border-4 border-white p-8 rounded-2xl shadow-lg"
// 						>
// 							<KolamDisplay
// 								pattern={currentPattern}
// 								animate={animationState === 'playing'}
// 								animationState={animationState}
// 								animationTiming={getAnimationTiming(animationSpeed)}
// 								className="kolam-main"
// 							/>

// 							{/* Download Menu */}
// 							{currentPattern && (
// 								<div className="absolute top-4 right-4">
// 									<div className="relative download-menu">
// 										<button
// 											onClick={() => setShowDownloadMenu(!showDownloadMenu)}
// 											disabled={isExporting}
// 											className="p-3 bg-[#f0c75e]/90 border-2 text-white rounded-lg hover:bg-[#f0c75e]/75 transition-colors disabled:opacity-50 shadow-lg backdrop-blur-sm"
// 											title="Download Options"
// 										>
// 											{isExporting ? '⏳' : '💾'}
// 										</button>

// 										{showDownloadMenu && (
// 											<div className="absolute right-0 mt-2 bg-[#2e2e3f] border-2 border-white rounded-lg shadow-lg py-1 z-10 min-w-[200px]">
// 												<button
// 													onClick={() => { exportPattern('svg'); setShowDownloadMenu(false); }}
// 													className="w-full text-left px-4 py-2 text-[#f0c75e] hover:bg-[#1e1e2f] transition-colors"
// 												>
// 													📄 Download SVG
// 												</button>
// 												<button
// 													onClick={() => { exportPattern('png'); setShowDownloadMenu(false); }}
// 													className="w-full text-left px-4 py-2 text-[#f0c75e] hover:bg-[#1e1e2f] transition-colors"
// 												>
// 													🖼️ Download PNG
// 												</button>
// 												<hr className="my-1 border-white" />
// 												<button
// 													onClick={() => { getEmbedCode(); setShowDownloadMenu(false); }}
// 													className="w-full text-left px-4 py-2 text-[#f0c75e] hover:bg-[#1e1e2f] transition-colors"
// 												>
// 													📋 Copy Embed Code
// 												</button>
// 												<button
// 													onClick={() => { copyRawSVG(); setShowDownloadMenu(false); }}
// 													className="w-full text-left px-4 py-2 text-[#f0c75e] hover:bg-[#1e1e2f] transition-colors"
// 												>
// 													📄 Copy Raw SVG
// 												</button>
// 											</div>
// 										)}
// 									</div>
// 								</div>
// 							)}
// 						</div>
// 					) : (
// 						<div className="no-pattern text-center py-12 bg-[#2e2e3f] border-2 border-white rounded-2xl">
// 							<p className="text-[#f0c75e] text-lg">Loading your first kolam...</p>
// 						</div>
// 					)}
// 				</div>

// 				{/* Controls */}
// 				<div className="bg-[#2e2e3f] border-4 border-white rounded-2xl p-6 mt-8">
// 					<h2 className="text-xl font-semibold mb-4 text-[#f0c75e] flex items-center">
// 						<span className="mr-2">⚙️</span>
// 						Kolam Parameters
// 					</h2>

// 					<div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
// 						{/* Size */}
// 						<div className="parameter-group">
// 							<label htmlFor="size" className="block text-sm font-medium text-[#f0c75e] mb-2">Grid Size</label>
// 							<div className="flex items-center space-x-3">
// 								<input
// 									id="size"
// 									type="range"
// 									min="3"
// 									max="15"
// 									value={size}
// 									onChange={(e) => setSize(parseInt(e.target.value))}
// 									className="flex-1"
// 									style={{ accentColor: '#f0c75e' }}
// 									/>
// 								<div className="bg-[#1e1e2f] px-3 py-1 rounded text-[#f0c75e] min-w-[3rem] text-center">{size}</div>
// 							</div>
// 							<div className="text-xs text-[#f0c75e] mt-1">Creates a {size}x{size} pattern grid</div>
// 						</div>

// 						{/* Animation Speed */}
// 						<div className="parameter-group">
// 							<label htmlFor="animationSpeed" className="block text-sm font-medium text-[#f0c75e] mb-2">Animation Duration</label>
// 							<div className="flex items-center space-x-3">
// 								<input
// 									id="animationSpeed"
// 									type="range"
// 									min="1"
// 									max="10"
// 									value={animationSpeed}
// 									onChange={(e) => setAnimationSpeed(parseInt(e.target.value))}
// 									className="flex-1"
// 									style={{ accentColor: '#f0c75e' }}
// 								/>
// 								<div className="bg-[#1e1e2f] px-3 py-1 rounded text-[#f0c75e] min-w-[3rem] text-center">{animationSpeed}</div>
// 							</div>
// 							<div className="text-xs text-[#f0c75e] mt-1">Total: {(animationDuration / 1000).toFixed(1)}s</div>
// 						</div>
// 					</div>

// 					{/* Buttons */}
// 					<div className="flex justify-center items-center gap-6">
// 						{currentPattern && (
// 							<button
// 								onClick={() => setAnimationState(animationState === 'playing' ? 'stopped' : 'playing')}
// 								className="px-6 py-3 bg-[#f0c75e] border-2 border-white text-[#1e1e2f] rounded-lg hover:opacity-90 transition-colors font-medium shadow-lg flex items-center gap-2"
// 							>
// 								{animationState === 'playing' ? '⏹️ Stop Animation' : '▶️ Play Animation'}
// 							</button>
// 						)}

// 						<button
// 							onClick={() => generatePattern()}
// 							className="px-8 py-3 border-2 border-white text-white rounded-lg hover:opacity-90 transition-colors font-medium shadow-lg"
// 							style={{ backgroundColor: '#5ba293' }}
// 						>
// 							Generate Kolam
// 						</button>
// 					</div>
// 				</div>
// 			</div>

// 			{/* Footer */}
// 			<footer className="p-6 text-white bg-[#1e1e2f] mt-12 rounded-t-lg">
// 				<div className="max-w-6xl mx-auto text-center">
// 					<p className="text-xl opacity-80">
// 						Created by Code Learners
// 					</p>
// 				</div>
// 			</footer>
// 		</div>
// 	);
// };



// 'use client';

// import { KolamPattern } from '@/types/kolam';
// import { KolamExporter } from '@/utils/kolamExporter';
// import { KolamGenerator } from '@/utils/kolamGenerator';
// import { durationToSpeed, generateEmbedURL, speedToDuration, updateURL, useKolamURLParams } from '@/utils/urlParams';
// import React, { useCallback, useEffect, useRef, useState } from 'react';
// import { KolamDisplay } from './KolamDisplay';

// export const KolamEditor: React.FC = () => {
//     const [currentPattern, setCurrentPattern] = useState<KolamPattern | null>(null);
//     const [isExporting, setIsExporting] = useState(false);
//     const [showDownloadMenu, setShowDownloadMenu] = useState(false);
//     const [animationState, setAnimationState] = useState<'stopped' | 'playing' | 'paused'>('stopped');
//     const kolamRef = useRef<HTMLDivElement>(null);

//     const urlParams = useKolamURLParams();
//     const [size, setSize] = useState(urlParams.size);
//     const [animationSpeed, setAnimationSpeed] = useState(durationToSpeed(urlParams.duration));
//     const [animationDuration, setAnimationDuration] = useState(urlParams.duration);
//     const [initialAutoAnimate, setInitialAutoAnimate] = useState(urlParams.initialAutoAnimate);

//     useEffect(() => {
//         updateURL({ size, duration: animationDuration, initialAutoAnimate });
//     }, [size, animationDuration, initialAutoAnimate]);

//     useEffect(() => {
//         const newDuration = speedToDuration(animationSpeed);
//         setAnimationDuration(newDuration);
//     }, [animationSpeed]);

//     useEffect(() => {
//         const handleClickOutside = (event: MouseEvent) => {
//             if (showDownloadMenu && !(event.target as Element).closest('.download-menu')) {
//                 setShowDownloadMenu(false);
//             }
//         };
//         document.addEventListener('mousedown', handleClickOutside);
//         return () => document.removeEventListener('mousedown', handleClickOutside);
//     }, [showDownloadMenu]);

//     useEffect(() => {
//         if (animationState === 'playing' && currentPattern) {
//             const timer = setTimeout(() => {
//                 setAnimationState('stopped');
//             }, animationDuration);
//             return () => clearTimeout(timer);
//         }
//     }, [animationState, currentPattern, animationDuration]);

//     const getAnimationTiming = (speed: number) => {
//         return speedToDuration(speed);
//     };

//     const generatePattern = useCallback(() => {
//         console.log('🎯 Generating kolam pattern');
//         try {
//             const pattern = KolamGenerator.generateKolam1D(size);
//             setCurrentPattern(pattern);
//             setAnimationState('stopped');

//             if (initialAutoAnimate) {
//                 setTimeout(() => setAnimationState('playing'), 100);
//             }
//         } catch (error) {
//             const errorMessage = error instanceof Error ? error.message : String(error);
//             alert(`Error generating pattern: ${errorMessage}`);
//         }
//     }, [size, initialAutoAnimate]);

//     useEffect(() => {
//         generatePattern();
//     }, [generatePattern]);

//     const exportPattern = async (format: 'svg' | 'png' | 'gif') => {
//         if (!currentPattern || !kolamRef.current) return;
//         setIsExporting(true);
//         try {
//             switch (format) {
//                 case 'svg':
//                     await KolamExporter.downloadSVG(currentPattern);
//                     break;
//                 case 'png':
//                     // Hide the download menu temporarily during PNG export
//                     const menu = document.querySelector('.download-menu');
//                     if (menu) menu.style.display = 'none';
//                     await KolamExporter.downloadPNG(kolamRef.current, currentPattern.name);
//                     if (menu) menu.style.display = '';
//                     break;
//                 case 'gif':
//                     await KolamExporter.downloadAnimatedGIF(
//                         kolamRef.current,
//                         currentPattern,
//                         currentPattern.name,
//                         { format: 'gif', frameCount: 30, delay: animationDuration }
//                     );
//                     break;
//             }
//         } catch (error) {
//             alert('Export failed. Please try again.');
//         } finally {
//             setIsExporting(false);
//         }
//     };

//     const getEmbedCode = async () => {
//         if (!currentPattern) return;
//         try {
//             const embedURL = generateEmbedURL({ size, background: '#1e1e2f', brush: '#00FFFF' });
//             const embedCode = `<img src="${embedURL}" alt="Kolam Pattern" style="max-width: 100%; height: auto;" />`;
//             await navigator.clipboard.writeText(embedCode);
//             alert('Embed code copied to clipboard!');
//         } catch (error) {
//             alert('Failed to copy embed code.');
//         }
//     };

//     const copyRawSVG = async () => {
//         if (!currentPattern) return;
//         try {
//             const svgContent = await KolamExporter.exportAsSVG(currentPattern);
//             await navigator.clipboard.writeText(svgContent);
//             alert('Raw SVG code copied to clipboard!');
//         } catch (error) {
//             alert('Failed to copy raw SVG.');
//         }
//     };

//     return (
//         <div className="kolam-editor bg-[#1e1e2f] text-white min-h-screen">
//             <header className="p-6" style={{ backgroundColor: '#5ba293' }}>
//                 <div className="max-w-6xl mx-auto">
//                     <h1 className="text-4xl font-bold text-center tracking-wide">Kolam Generator</h1>
//                     <p className="text-center mt-2 text-lg opacity-90">
//                         Generate beautiful traditional South Indian Kolam patterns
//                     </p>
//                 </div>
//             </header>

//             <div className="max-w-6xl mx-auto p-8">
//                 <div className="kolam-display-area">
//                     {currentPattern ? (
//                         <div
//                             ref={kolamRef}
//                             className="kolam-container relative flex justify-center items-center bg-[#2e2e3f] border-4 border-white p-8 rounded-2xl shadow-lg"
//                         >
//                             <KolamDisplay
//                                 pattern={currentPattern}
//                                 animate={animationState === 'playing'}
//                                 animationState={animationState}
//                                 animationTiming={getAnimationTiming(animationSpeed)}
//                                 className="kolam-main"
//                             />

//                             {currentPattern && (
//                                 <div className="absolute top-4 right-4">
//                                     <div className="relative download-menu">
//                                         <button
//                                             onClick={() => setShowDownloadMenu(!showDownloadMenu)}
//                                             disabled={isExporting}
//                                             className="p-3 bg-[#f0c75e]/90 border-2 text-white rounded-lg hover:bg-[#f0c75e]/75 transition-colors disabled:opacity-50 shadow-lg backdrop-blur-sm"
//                                             title="Download Options"
//                                         >
//                                             {isExporting ? '⏳' : '💾'}
//                                         </button>

//                                         {showDownloadMenu && (
//                                             <div className="absolute right-0 mt-2 bg-[#2e2e3f] border-2 border-white rounded-lg shadow-lg py-1 z-10 min-w-[200px]">
//                                                 <button
//                                                     onClick={() => { exportPattern('svg'); setShowDownloadMenu(false); }}
//                                                     className="w-full text-left px-4 py-2 text-[#f0c75e] hover:bg-[#1e1e2f] transition-colors"
//                                                 >
//                                                     📄 Download SVG
//                                                 </button>
//                                                 <button
//                                                     onClick={() => { exportPattern('png'); setShowDownloadMenu(false); }}
//                                                     className="w-full text-left px-4 py-2 text-[#f0c75e] hover:bg-[#1e1e2f] transition-colors"
//                                                 >
//                                                     🖼️ Download PNG
//                                                 </button>
//                                                 <hr className="my-1 border-white" />
//                                                 <button
//                                                     onClick={() => { getEmbedCode(); setShowDownloadMenu(false); }}
//                                                     className="w-full text-left px-4 py-2 text-[#f0c75e] hover:bg-[#1e1e2f] transition-colors"
//                                                 >
//                                                     📋 Copy Embed Code
//                                                 </button>
//                                                 <button
//                                                     onClick={() => { copyRawSVG(); setShowDownloadMenu(false); }}
//                                                     className="w-full text-left px-4 py-2 text-[#f0c75e] hover:bg-[#1e1e2f] transition-colors"
//                                                 >
//                                                     📄 Copy Raw SVG
//                                                 </button>
//                                             </div>
//                                         )}
//                                     </div>
//                                 </div>
//                             )}
//                         </div>
//                     ) : (
//                         <div className="no-pattern text-center py-12 bg-[#2e2e3f] border-2 border-white rounded-2xl">
//                             <p className="text-[#f0c75e] text-lg">Loading your first kolam...</p>
//                         </div>
//                     )}
//                 </div>

//                 {/* Controls */}
//                 <div className="bg-[#2e2e3f] border-4 border-white rounded-2xl p-6 mt-8">
//                     <h2 className="text-xl font-semibold mb-4 text-[#f0c75e] flex items-center">
//                         <span className="mr-2">⚙️</span>
//                         Kolam Parameters
//                     </h2>

//                     <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
//                         {/* Size */}
//                         <div className="parameter-group">
//                             <label htmlFor="size" className="block text-sm font-medium text-[#f0c75e] mb-2">Grid Size</label>
//                             <div className="flex items-center space-x-3">
//                                 <input
//                                     id="size"
//                                     type="range"
//                                     min="3"
//                                     max="15"
//                                     value={size}
//                                     onChange={(e) => setSize(parseInt(e.target.value))}
//                                     className="flex-1"
//                                     style={{ accentColor: '#f0c75e' }}
//                                 />
//                                 <div className="bg-[#1e1e2f] px-3 py-1 rounded text-[#f0c75e] min-w-[3rem] text-center">{size}</div>
//                             </div>
//                             <div className="text-xs text-[#f0c75e] mt-1">Creates a {size}x{size} pattern grid</div>
//                         </div>

//                         {/* Animation Speed */}
//                         <div className="parameter-group">
//                             <label htmlFor="animationSpeed" className="block text-sm font-medium text-[#f0c75e] mb-2">Animation Duration</label>
//                             <div className="flex items-center space-x-3">
//                                 <input
//                                     id="animationSpeed"
//                                     type="range"
//                                     min="1"
//                                     max="10"
//                                     value={animationSpeed}
//                                     onChange={(e) => setAnimationSpeed(parseInt(e.target.value))}
//                                     className="flex-1"
//                                     style={{ accentColor: '#f0c75e' }}
//                                 />
//                                 <div className="bg-[#1e1e2f] px-3 py-1 rounded text-[#f0c75e] min-w-[3rem] text-center">{animationSpeed}</div>
//                             </div>
//                             <div className="text-xs text-[#f0c75e] mt-1">Total: {(animationDuration / 1000).toFixed(1)}s</div>
//                         </div>
//                     </div>

//                     {/* Buttons */}
//                     <div className="flex justify-center items-center gap-6">
//                         {currentPattern && (
//                             <button
//                                 onClick={() => setAnimationState(animationState === 'playing' ? 'stopped' : 'playing')}
//                                 className="px-6 py-3 bg-[#f0c75e] border-2 border-white text-[#1e1e2f] rounded-lg hover:opacity-90 transition-colors font-medium shadow-lg flex items-center gap-2"
//                             >
//                                 {animationState === 'playing' ? '⏹️ Stop Animation' : '▶️ Play Animation'}
//                             </button>
//                         )}

//                         <button
//                             onClick={() => generatePattern()}
//                             className="px-8 py-3 border-2 border-white text-white rounded-lg hover:opacity-90 transition-colors font-medium shadow-lg"
//                             style={{ backgroundColor: '#5ba293' }}
//                         >
//                             Generate Kolam
//                         </button>
//                     </div>
//                 </div>
//             </div>

//             {/* Footer */}
//             <footer className="p-6 text-white bg-[#1e1e2f] mt-12 rounded-t-lg">
//                 <div className="max-w-6xl mx-auto text-center">
//                     <p className="text-xl opacity-80">
//                         Created by Code Learners
//                     </p>
//                 </div>
//             </footer>
//         </div>
//     );
// };

'use client';

import { KolamPattern } from '@/types/kolam';
import { KolamExporter } from '@/utils/kolamExporter';
import { KolamGenerator } from '@/utils/kolamGenerator';
import { durationToSpeed, generateEmbedURL, speedToDuration, updateURL, useKolamURLParams } from '@/utils/urlParams';
import React, { useCallback, useEffect, useRef, useState } from 'react';
import { KolamDisplay } from './KolamDisplay';

export const KolamEditor: React.FC = () => {
    const [currentPattern, setCurrentPattern] = useState<KolamPattern | null>(null);
    const [isExporting, setIsExporting] = useState(false);
    const [showDownloadMenu, setShowDownloadMenu] = useState(false);
    const [animationState, setAnimationState] = useState<'stopped' | 'playing' | 'paused'>('stopped');
    const kolamRef = useRef<HTMLDivElement>(null);

    const urlParams = useKolamURLParams();
    const [size, setSize] = useState(urlParams.size);
    const [animationSpeed, setAnimationSpeed] = useState(durationToSpeed(urlParams.duration));
    const [animationDuration, setAnimationDuration] = useState(urlParams.duration);
    const [initialAutoAnimate, setInitialAutoAnimate] = useState(urlParams.initialAutoAnimate);

    useEffect(() => {
        updateURL({ size, duration: animationDuration, initialAutoAnimate });
    }, [size, animationDuration, initialAutoAnimate]);

    useEffect(() => {
        const newDuration = speedToDuration(animationSpeed);
        setAnimationDuration(newDuration);
    }, [animationSpeed]);

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (showDownloadMenu && !(event.target as Element).closest('.download-menu')) {
                setShowDownloadMenu(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, [showDownloadMenu]);

    useEffect(() => {
        if (animationState === 'playing' && currentPattern) {
            const timer = setTimeout(() => {
                setAnimationState('stopped');
            }, animationDuration);
            return () => clearTimeout(timer);
        }
    }, [animationState, currentPattern, animationDuration]);

    const getAnimationTiming = (speed: number) => {
        return speedToDuration(speed);
    };

    const generatePattern = useCallback(() => {
        console.log('🎯 Generating kolam pattern');
        try {
            const pattern = KolamGenerator.generateKolam1D(size);
            setCurrentPattern(pattern);
            setAnimationState('stopped');

            if (initialAutoAnimate) {
                setTimeout(() => setAnimationState('playing'), 100);
            }
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : String(error);
            alert(`Error generating pattern: ${errorMessage}`);
        }
    }, [size, initialAutoAnimate]);

    useEffect(() => {
        generatePattern();
    }, [generatePattern]);

    const exportPattern = async (format: 'svg' | 'png' | 'gif') => {
        if (!currentPattern || !kolamRef.current) return;
        setIsExporting(true);
        try {
            switch (format) {
                case 'svg':
                    await KolamExporter.downloadSVG(currentPattern);
                    break;
                case 'png':
                    const menu = document.querySelector('.download-menu');
                    if (menu) menu.style.display = 'none';
                    await KolamExporter.downloadPNG(kolamRef.current, currentPattern.name);
                    if (menu) menu.style.display = '';
                    break;
                case 'gif':
                    await KolamExporter.downloadAnimatedGIF(
                        kolamRef.current,
                        currentPattern,
                        currentPattern.name,
                        { format: 'gif', frameCount: 30, delay: animationDuration }
                    );
                    break;
            }
        } catch (error) {
            alert('Export failed. Please try again.');
        } finally {
            setIsExporting(false);
        }
    };

    const getEmbedCode = async () => {
        if (!currentPattern) return;
        try {
            const embedURL = generateEmbedURL({ size, background: '#1e1e2f', brush: '#00FFFF' });
            const embedCode = `<img src="${embedURL}" alt="Kolam Pattern" style="max-width: 100%; height: auto;" />`;
            await navigator.clipboard.writeText(embedCode);
            alert('Embed code copied to clipboard!');
        } catch (error) {
            alert('Failed to copy embed code.');
        }
    };

    const copyRawSVG = async () => {
        if (!currentPattern) return;
        try {
            const svgContent = await KolamExporter.exportAsSVG(currentPattern);
            await navigator.clipboard.writeText(svgContent);
            alert('Raw SVG code copied to clipboard!');
        } catch (error) {
            alert('Failed to copy raw SVG.');
        }
    };

    return (
        <div className="kolam-editor bg-[#1e1e2f] text-white min-h-screen">
            <header className="p-6" style={{ backgroundColor: '#5ba293' }}>
                <div className="max-w-6xl mx-auto">
                    <h1 className="text-4xl font-bold text-center tracking-wide">Kolam Generator</h1>
                    <p className="text-center mt-2 text-lg opacity-90">
                        Generate beautiful traditional South Indian Kolam patterns
                    </p>
                </div>
            </header>

            <div className="max-w-6xl mx-auto p-8">
                <div className="kolam-display-area">
                    {currentPattern ? (
                        <div
                            ref={kolamRef}
                            className="kolam-container relative flex justify-center items-center bg-[#2e2e3f] p-8 rounded-2xl shadow-lg"
                        >
                            <KolamDisplay
                                pattern={currentPattern}
                                animate={animationState === 'playing'}
                                animationState={animationState}
                                animationTiming={getAnimationTiming(animationSpeed)}
                                className="kolam-main"
                            />

                            {currentPattern && (
                                <div className="absolute top-4 right-4">
                                    <div className="relative download-menu">
                                        <button
                                            onClick={() => setShowDownloadMenu(!showDownloadMenu)}
                                            disabled={isExporting}
                                            className="p-3 bg-[#f0c75e]/90 border-2 text-white rounded-lg hover:bg-[#f0c75e]/75 transition-colors disabled:opacity-50 shadow-lg backdrop-blur-sm"
                                            title="Download Options"
                                        >
                                            {isExporting ? '⏳' : '💾'}
                                        </button>

                                        {showDownloadMenu && (
                                            <div className="absolute right-0 mt-2 bg-[#2e2e3f] border-2 border-white rounded-lg shadow-lg py-1 z-10 min-w-[200px]">
                                                <button
                                                    onClick={() => { exportPattern('svg'); setShowDownloadMenu(false); }}
                                                    className="w-full text-left px-4 py-2 text-[#f0c75e] hover:bg-[#1e1e2f] transition-colors"
                                                >
                                                    📄 Download SVG
                                                </button>
                                                <button
                                                    onClick={() => { exportPattern('png'); setShowDownloadMenu(false); }}
                                                    className="w-full text-left px-4 py-2 text-[#f0c75e] hover:bg-[#1e1e2f] transition-colors"
                                                >
                                                    🖼️ Download PNG
                                                </button>
                                                <hr className="my-1 border-white" />
                                                <button
                                                    onClick={() => { getEmbedCode(); setShowDownloadMenu(false); }}
                                                    className="w-full text-left px-4 py-2 text-[#f0c75e] hover:bg-[#1e1e2f] transition-colors"
                                                >
                                                    📋 Copy Embed Code
                                                </button>
                                                <button
                                                    onClick={() => { copyRawSVG(); setShowDownloadMenu(false); }}
                                                    className="w-full text-left px-4 py-2 text-[#f0c75e] hover:bg-[#1e1e2f] transition-colors"
                                                >
                                                    📄 Copy Raw SVG
                                                </button>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="no-pattern text-center py-12 bg-[#2e2e3f] border-2 border-white rounded-2xl">
                            <p className="text-[#f0c75e] text-lg">Loading your first kolam...</p>
                        </div>
                    )}
                </div>

                {/* Controls */}
                <div className="bg-[#2e2e3f] border-4 border-white rounded-2xl p-6 mt-8">
                    <h2 className="text-xl font-semibold mb-4 text-[#f0c75e] flex items-center">
                        <span className="mr-2">⚙️</span>
                        Kolam Parameters
                    </h2>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                        {/* Size */}
                        <div className="parameter-group">
                            <label htmlFor="size" className="block text-sm font-medium text-[#f0c75e] mb-2">Grid Size</label>
                            <div className="flex items-center space-x-3">
                                <input
                                    id="size"
                                    type="range"
                                    min="3"
                                    max="15"
                                    value={size}
                                    onChange={(e) => setSize(parseInt(e.target.value))}
                                    className="flex-1"
                                    style={{ accentColor: '#f0c75e' }}
                                />
                                <div className="bg-[#1e1e2f] px-3 py-1 rounded text-[#f0c75e] min-w-[3rem] text-center">{size}</div>
                            </div>
                            <div className="text-xs text-[#f0c75e] mt-1">Creates a {size}x{size} pattern grid</div>
                        </div>

                        {/* Animation Speed */}
                        <div className="parameter-group">
                            <label htmlFor="animationSpeed" className="block text-sm font-medium text-[#f0c75e] mb-2">Animation Duration</label>
                            <div className="flex items-center space-x-3">
                                <input
                                    id="animationSpeed"
                                    type="range"
                                    min="1"
                                    max="10"
                                    value={animationSpeed}
                                    onChange={(e) => setAnimationSpeed(parseInt(e.target.value))}
                                    className="flex-1"
                                    style={{ accentColor: '#f0c75e' }}
                                />
                                <div className="bg-[#1e1e2f] px-3 py-1 rounded text-[#f0c75e] min-w-[3rem] text-center">{animationSpeed}</div>
                            </div>
                            <div className="text-xs text-[#f0c75e] mt-1">Total: {(animationDuration / 1000).toFixed(1)}s</div>
                        </div>
                    </div>

                    {/* Buttons */}
                    <div className="flex justify-center items-center gap-6">
                        {currentPattern && (
                            <button
                                onClick={() => setAnimationState(animationState === 'playing' ? 'stopped' : 'playing')}
                                className="px-6 py-3 bg-[#f0c75e] border-2 border-white text-[#1e1e2f] rounded-lg hover:opacity-90 transition-colors font-medium shadow-lg flex items-center gap-2"
                            >
                                {animationState === 'playing' ? '⏹️ Stop Animation' : '▶️ Play Animation'}
                            </button>
                        )}
                        <button
                            onClick={() => generatePattern()}
                            className="px-8 py-3 border-2 border-white text-white rounded-lg hover:opacity-90 transition-colors font-medium shadow-lg"
                            style={{ backgroundColor: '#5ba293' }}
                        >
                            Generate Kolam
                        </button>
                    </div>
                </div>
            </div>
            <footer className="p-6 text-white bg-[#1e1e2f] mt-12 rounded-t-lg">
                <div className="max-w-6xl mx-auto text-center">
                    <p className="text-xl opacity-80">
                        Created by Code Learners
                    </p>
                </div>
            </footer>
        </div>
    );
};
