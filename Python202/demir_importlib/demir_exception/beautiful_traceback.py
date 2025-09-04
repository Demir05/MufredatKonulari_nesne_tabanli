"""
amacımız hata çıktısını şık ve özelleştirmesini kolay hale getirmek\n
"""
import types
from typing import *

def better_frame(exception: BaseException):

    def walk() -> List[types.TracebackType]|None:

        buffer: List[types.TracebackType] = []
        

        __traceback: types.TracebackType  = exception.__traceback__ # type: ignore

        while __traceback:
            buffer.append(__traceback) # type: ignore
            
            __traceback: types.FrameType|None = __traceback.tb_next # type: ignore

        return buffer if buffer else None


    def formatter():
        
        
        def keygenerator(traceback: types.TracebackType) -> str:
            return f"{traceback.tb_frame.f_code.co_filename}.{traceback.tb_frame.f_code.co_qualname}"
        
        walked_tracebacks: List[types.TracebackType]|None
        
        if (walked_tracebacks := walk()) is None:
            return None

        buffer: Dict[Any, Any] = {}
    
        
        for frame_num, trace in enumerate(walked_tracebacks,1):
            buffer.update(
    dict(
        idx=frame_num,
        key=keygenerator(trace),
        meta=dict(
            filename=trace.tb_frame.f_code.co_filename,
            lineno=trace.tb_lineno,
            func_name=trace.tb_frame.f_code.co_name,
            qualname=getattr(trace.tb_frame.f_code, "co_qualname", None),
            module=trace.tb_frame.f_globals.get("__name__"),
            firstlineno=trace.tb_frame.f_code.co_firstlineno,
            lasti=trace.tb_frame.f_lasti,
            frame_id=id(trace.tb_frame),
            # kısa özet: local isimler ve tipleri (hassas veriyi loglamamaya dikkat)
            locals_summary={k: type(v).__name__ for k, v in list(trace.tb_frame.f_locals.items())[:12]},
            # globals için sadece anahtar listesi (büyük/tehlikeli objelerden kaçın)
            globals_keys=list(trace.tb_frame.f_globals.keys())[:40],
            # kod objesi hakkında küçük özet
            code_info=dict(
                argnames=tuple(trace.tb_frame.f_code.co_varnames[: trace.tb_frame.f_code.co_argcount]),
                argcount=trace.tb_frame.f_code.co_argcount,
                flags=trace.tb_frame.f_code.co_flags,
            ),
            # küçük kaynak snippet (dosya okunabilir değilse None olacak şekilde)
            source_snippet=None,  # isteğe göre linecache/inspect ile 3-5 satır eklensin
        ),
    )
)       
        return buffer    
           
    return formatter()
    
try:
    def f(): 1 / 0
    def g(): f()
    g()
except Exception as e:
    from pprint import pprint
    pprint(better_frame(e))
