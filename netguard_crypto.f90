subroutine batch_crack(wordlist_matrix, rows, cols, target_hash, found_row_index)
    implicit none
    integer, intent(in) :: rows, cols
    integer(kind=8), intent(in) :: target_hash
    integer, dimension(cols, rows), intent(in) :: wordlist_matrix
    integer, intent(out) :: found_row_index
    integer :: i, j
    integer(kind=8) :: current_sum
    
    found_row_index = -1
    
    do i = 1, rows
        current_sum = 0
        do j = 1, cols
            current_sum = current_sum + wordlist_matrix(j, i)
        end do
        
        if (current_sum == target_hash) then
            found_row_index = i
            return
        end if
    end do
end subroutine batch_crack
