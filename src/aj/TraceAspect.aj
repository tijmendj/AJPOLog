package aj;

import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.JoinPoint.StaticPart;

import aj.Trace;

public aspect TraceAspect {
    pointcut traceMethods(Object o) : call(* *.*(..))
    	&& !within(TraceAspect)
    	&& !within(aj.*)
    	&& target(o);

    before(Object o): traceMethods(o) {
        JoinPoint joinpoint = thisJoinPoint;
        StaticPart enclosingJoinPoint = thisEnclosingJoinPointStaticPart;
        Trace.logMethodCall("Entry", joinpoint, enclosingJoinPoint, o, joinpoint.getStaticPart());
    }
    
    after(Object o) returning: traceMethods(o){
        JoinPoint joinpoint = thisJoinPoint;
        StaticPart enclosingJoinPoint = thisEnclosingJoinPointStaticPart;
        Trace.logMethodCall("Exit", joinpoint, enclosingJoinPoint, o, joinpoint.getStaticPart());
    }

}
